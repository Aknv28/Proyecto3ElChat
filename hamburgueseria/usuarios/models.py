from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    # Agregar campos adicionales, como 'rol'
    rol = models.CharField(
        max_length=20,
        choices=[('admin', 'Admin'), ('cocinero', 'Cocinero'), ('cajero', 'Cajero')],
        default='cajero'
    )
    carnet = models.CharField(max_length=20, unique=True, blank=True, null=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)  # Nuevo campo: fecha de nacimiento
    telefono = models.CharField(max_length=15, blank=True, null=True)  # Nuevo campo: teléfono
    direccion = models.CharField(max_length=255, blank=True, null=True)  # Nuevo campo: dirección

    def __str__(self):
        return self.username
