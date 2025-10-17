from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import uuid

# Modelo de Producto
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

    def __str__(self):
        return self.nombre

# Modelo de Cliente
class Cliente(models.Model):
    nombre = models.CharField(max_length=120)
    email = models.EmailField()
    telefono = models.CharField(max_length=40)

    def __str__(self):
        return self.nombre

# Modelo de Pedido
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
        editable=False)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    estado_actual = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='pendiente')
    total_monetario = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cliente = models.ForeignKey('Cliente', null=True, on_delete=models.SET_NULL)
    cajero = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.RESTRICT)  # Aquí cambiamos a settings.AUTH_USER_MODEL
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.numero_pedido

# Modelo de PedidoDetalle
class PedidoDetalle(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.producto.nombre} x {self.cantidad}'
