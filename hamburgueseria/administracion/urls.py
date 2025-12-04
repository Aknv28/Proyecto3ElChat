# administracion/urls.py

from django.urls import path
from django.views.decorators.cache import never_cache
from . import views

from .admin_reportes import reportes_dashboard

app_name = 'administracion'

urlpatterns = [
    # ============================================
    # DASHBOARD DE ADMINISTRADOR
    # ============================================
    path('dashboard/', never_cache(views.admin_dashboard), name='dashboard'),
    
    path("reportes/", reportes_dashboard, name="admin_reportes"),
    
    # Nota: El CRUD de usuarios se mantiene en usuarios.urls.py
    # pero se accede desde este módulo con permisos de administrador

]