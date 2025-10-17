from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario  # Asegúrate de importar el modelo Usuario

# Personalizar la clase UserAdmin para agregar el campo 'rol'
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('username', 'email', 'rol', 'is_active', 'is_staff')  # Campos a mostrar en la lista
    list_filter = ('is_active', 'rol')  # Permitir filtrado por 'rol'
    search_fields = ('username', 'email')  # Campos en los que buscar
    ordering = ('username',)  # Ordenar por 'username'
    
    # Especificamos los campos adicionales en el formulario de creación y edición de usuarios
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('rol',)}),  # Agregar el campo 'rol'
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('rol',)}),  # Agregar el campo 'rol' en el formulario de creación
    )

# Registrar el modelo con la configuración personalizada
admin.site.register(Usuario, UsuarioAdmin)
