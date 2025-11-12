# administracion/urls.py

from django.urls import path
from django.views.decorators.cache import never_cache
from . import views

app_name = 'administracion'

urlpatterns = [
    # ============================================
    # DASHBOARD DE ADMINISTRADOR
    # ============================================
    path('dashboard/', never_cache(views.admin_dashboard), name='dashboard'),
    
    # Nota: El CRUD de usuarios se mantiene en usuarios.urls.py
    # pero se accede desde este módulo con permisos de administrador
]