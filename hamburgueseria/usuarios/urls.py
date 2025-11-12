# usuarios/urls.py

from django.urls import path
from django.views.decorators.cache import never_cache
from . import views

app_name = 'usuarios'

urlpatterns = [
    # ============================================
    # AUTENTICACIÓN
    # ============================================
    path('login/', never_cache(views.login_view), name='login'),
    path('logout/', never_cache(views.logout_view), name='logout'),

    # ============================================
    # PÁGINAS PÚBLICAS
    # ============================================
    path('', views.index, name='index'),
    path('sobre_nosotros/', views.sobre_nosotros, name='sobre_nosotros'),
    path('servicios/', views.servicios, name='servicios'),
    path('contactanos/', views.contactanos, name='contactanos'),

    # ============================================
    # CRUD DE USUARIOS (solo para administradores)
    # Estas rutas permanecen aquí porque son gestión de usuarios
    # pero solo son accesibles desde el módulo de administración
    # ============================================
    path('usuarios/', never_cache(views.lista_usuarios), name='lista_usuarios'),
    path('usuarios/crear/', never_cache(views.crear_usuario), name='crear_usuario'),
    path('usuarios/editar/<int:id>/', never_cache(views.editar_usuario), name='editar_usuario'),
    path('usuarios/eliminar/<int:id>/', never_cache(views.eliminar_usuario), name='eliminar_usuario'),
    
    # ============================================
    # RUTAS DE PRUEBA PARA PÁGINAS DE ERROR
    # ⚠️ IMPORTANTE: Eliminar estas rutas en producción
    # ============================================
    path('test-404/', views.test_404, name='test_404'),
    path('test-500/', views.test_500, name='test_500'),
    path('test-403/', views.test_403, name='test_403'),
]