from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import uuid
from django.utils import timezone

# -------------------------------
# MODELOS BASE
# -------------------------------

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen_url = models.URLField(max_length=255)
    activo = models.BooleanField(default=True)
    tiempo_preparacion = models.FloatField(default=5.0)

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    nombre = models.CharField(max_length=120)
    email = models.EmailField()
    telefono = models.CharField(max_length=40)

    def __str__(self):
        return self.nombre


# -------------------------------
# MODELOS DE PEDIDO Y DETALLE
# -------------------------------

class Pedido(models.Model):
    TIPO_CHOICES = (
        ('local', 'Comer en el local'),
        ('llevar', 'Para llevar'),
    )

    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('en_cocina', 'En cocina'),
        ('listo', 'Listo'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    )

    numero_pedido = models.CharField(
        max_length=100,
        unique=True,
        default=uuid.uuid4,
        editable=False
    )
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    estado_actual = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='pendiente')
    total_monetario = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cliente = models.ForeignKey('Cliente', null=True, on_delete=models.SET_NULL)
    cajero = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    # Campos para teoría de colas
    prioridad = models.FloatField(default=0.0)
    tiempo_estimado_total = models.FloatField(default=0.0)
    tiempo_espera = models.FloatField(default=0.0)
    # 🔹 NUEVO: Marca si está en preparación activa (posición 1 fija)
    en_preparacion = models.BooleanField(default=False)

    def __str__(self):
        return f"Pedido {self.numero_pedido}"

    def cantidad_hamburguesas(self):
        """Calcula la cantidad total de hamburguesas del pedido"""
        return sum(
            d.cantidad for d in self.detalles.filter(producto__categoria_id=1)
        )

    def calcular_tiempo_estimado(self):
        """
        Calcula el tiempo total estimado de preparación.
        Solo considera hamburguesas (categoría_id=1)
        """
        total = 0
        for detalle in self.detalles.filter(producto__categoria_id=1):
            total += detalle.producto.tiempo_preparacion * detalle.cantidad
        self.tiempo_estimado_total = total
        return total

    def calcular_prioridad(self, 
                          peso_tiempo=0.4, 
                          peso_tipo=0.1, 
                          peso_eficiencia=0.1,
                          peso_urgencia=0.4):
        """
        🔥 ALGORITMO MEJORADO DE PRIORIZACIÓN - M/M/1 CON AJUSTES
        
        📌 CAMBIOS PRINCIPALES:
        1. ✅ Pedido en preparación = Prioridad 999 (FIJA, no se mueve)
        2. ✅ Penaliza pedidos muy pequeños (1-2 hamburguesas)
        3. ✅ Da peso extra a pedidos "para llevar"
        4. ✅ Considera tiempo de espera vs tiempo estimado
        5. ✅ Balance entre eficiencia y justicia
        
        Parámetros ajustables:
        - peso_tiempo: Importancia del tiempo de espera (default 0.35)
        - peso_tipo: Importancia del tipo de pedido (default 0.25)
        - peso_eficiencia: Balance cantidad/tiempo (default 0.25)
        - peso_urgencia: Pedidos que exceden tiempo esperado (default 0.15)
        """
        # 🔹 REGLA 1: Si está en preparación, prioridad máxima fija
        if self.en_preparacion:
            self.prioridad = 999.0
            return 999.0
        
        cantidad = self.cantidad_hamburguesas()
        
        if cantidad == 0:
            self.prioridad = 0
            return 0
        
        # Calcular tiempo de espera actual
        tiempo_espera_min = (timezone.now() - self.creado_en).total_seconds() / 60
        self.tiempo_espera = tiempo_espera_min
        
        # ════════════════════════════════════════════════════════
        # COMPONENTE 1: FACTOR DE TIEMPO DE ESPERA (0-10 puntos)
        # ════════════════════════════════════════════════════════
        # Crece exponencialmente con el tiempo
        # A los 3 min = ~1 punto, a los 9 min = ~3 puntos, a los 15 min = ~5 puntos
        factor_tiempo = min(10, (tiempo_espera_min / 3) ** 1.2)
        
        # ════════════════════════════════════════════════════════
        # COMPONENTE 2: FACTOR DE TIPO DE PEDIDO (0-10 puntos)
        # ════════════════════════════════════════════════════════
        # "Para llevar" tiene más urgencia (cliente esperando de pie)
        # "En local" tiene menos urgencia (cliente sentado)
        if self.tipo == 'llevar':
            factor_tipo = 8.0  # Alta prioridad
        else:
            factor_tipo = 3.0  # Prioridad normal
        
        # ════════════════════════════════════════════════════════
        # COMPONENTE 3: FACTOR DE EFICIENCIA (0-10 puntos)
        # ════════════════════════════════════════════════════════
        # Balance entre tamaño del pedido y tiempo de preparación
        
        tiempo_promedio_por_unidad = self.tiempo_estimado_total / cantidad if cantidad > 0 else 0
        
        # 🔸 Penalización/bonus según tamaño del pedido
        if cantidad == 1:
            ajuste_cantidad = 0.4  # Penaliza mucho pedidos de 1 sola
        elif cantidad == 2:
            ajuste_cantidad = 0.65  # Penaliza pedidos de 2
        elif cantidad <= 4:
            ajuste_cantidad = 1.0  # Pedidos medianos, óptimos
        elif cantidad <= 6:
            ajuste_cantidad = 0.95  # Pedidos grandes, ligeramente menos
        else:
            ajuste_cantidad = 0.85  # Pedidos muy grandes
        
        # 🔸 Ajuste por tiempo de preparación individual
        if tiempo_promedio_por_unidad < 5:
            base_eficiencia = 8.0  # Hamburguesas rápidas
        elif tiempo_promedio_por_unidad < 6:
            base_eficiencia = 6.5  # Tiempo normal
        else:
            base_eficiencia = 5.0  # Hamburguesas complejas
        
        factor_eficiencia = base_eficiencia * ajuste_cantidad
        
        # ════════════════════════════════════════════════════════
        # COMPONENTE 4: FACTOR DE URGENCIA (0-10 puntos)
        # ════════════════════════════════════════════════════════
        # Se activa cuando el tiempo de espera excede el tiempo estimado
        
        tiempo_esperado_max = self.tiempo_estimado_total * 1.3  # 30% de margen
        
        if tiempo_espera_min > tiempo_esperado_max + 10:
            factor_urgencia = 10.0  # CRÍTICO: +10 min de retraso
        elif tiempo_espera_min > tiempo_esperado_max + 5:
            factor_urgencia = 7.5   # ALTO: +5 min de retraso
        elif tiempo_espera_min > tiempo_esperado_max:
            factor_urgencia = 5.0   # MEDIO: Excedió tiempo esperado
        elif tiempo_espera_min > tiempo_esperado_max * 0.7:
            factor_urgencia = 2.0   # BAJO: Cerca del límite
        else:
            factor_urgencia = 0.5   # NORMAL: Dentro del tiempo
        
        # ════════════════════════════════════════════════════════
        # CÁLCULO FINAL DE PRIORIDAD (Escala 0-10)
        # ════════════════════════════════════════════════════════
        prioridad_total = (
            factor_tiempo * peso_tiempo +
            factor_tipo * peso_tipo +
            factor_eficiencia * peso_eficiencia +
            factor_urgencia * peso_urgencia
        )
        
        self.prioridad = round(prioridad_total, 2)
        return self.prioridad


class PedidoDetalle(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.producto.nombre} x {self.cantidad}'