from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import uuid
from datetime import datetime

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
    # 🔹 Campo nuevo: tiempo de preparación en minutos
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

    # 🔹 Campos adicionales para teoría de colas
    prioridad = models.FloatField(default=0.0)
    tiempo_estimado_total = models.FloatField(default=0.0)  # en minutos
    tiempo_espera = models.FloatField(default=0.0)  # tiempo en minutos desde que llegó

    def __str__(self):
        return f"Pedido {self.numero_pedido}"

    # 🔸 Calcular la cantidad de hamburguesas (categoría id=1)
    def cantidad_hamburguesas(self):
        return sum(
            d.cantidad for d in self.detalles.filter(producto__categoria_id=1)
        )

    # 🔸 Calcular tiempo total de preparación de hamburguesas
    def calcular_tiempo_estimado(self):
        total = 0
        for detalle in self.detalles.filter(producto__categoria_id=1):
            total += detalle.producto.tiempo_preparacion * detalle.cantidad
        self.tiempo_estimado_total = total
        return total

    # 🔸 Calcular prioridad dinámica (M/M/1 con prioridad no preemptiva)
    def calcular_prioridad(self, alpha=0.01):
        cantidad = self.cantidad_hamburguesas()
    # Usa timezone.now() para compatibilidad con USE_TZ=True
        tiempo_espera_min = (timezone.now() - self.creado_en).total_seconds() / 60
        self.tiempo_espera = tiempo_espera_min

        if cantidad == 0:
            self.prioridad = 0
        else:
            self.prioridad = (1 / cantidad) + (alpha * tiempo_espera_min)
        return self.prioridad


class PedidoDetalle(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.producto.nombre} x {self.cantidad}'
