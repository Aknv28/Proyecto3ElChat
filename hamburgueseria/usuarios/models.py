# usuarios/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    # Agregar campos adicionales, como 'rol'
    rol = models.CharField(
        max_length=20,
        choices=[('admin', 'Admin'), ('cocinero', 'Cocinero'), ('cajero', 'Cajero')],
        default='cajero'
    )

    def __str__(self):
        return self.username
