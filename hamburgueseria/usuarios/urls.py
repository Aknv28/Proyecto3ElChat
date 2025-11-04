from django.urls import path
from django.views.decorators.cache import never_cache
from . import views

urlpatterns = [
    # ============================================
    # AUTENTICACIÓN
    # ============================================
    path('login/', never_cache(views.login_view), name='login'),
    path('logout/', never_cache(views.logout_view), name='logout'),
    
    # ============================================
    # DASHBOARDS PROTEGIDOS (sin cache)
    # ============================================
    path('admin_dashboard/', never_cache(views.admin_dashboard), name='admin_dashboard'),
    path('cocinero_dashboard/', never_cache(views.cocinero_dashboard), name='cocinero_dashboard'),
    path('cajero_dashboard/', never_cache(views.cajero_dashboard), name='cajero_dashboard'),

    # ============================================
    # CRUD DE USUARIOS (solo para administradores)
    # ============================================
    path('usuarios/', never_cache(views.lista_usuarios), name='lista_usuarios'),
    path('usuarios/crear/', never_cache(views.crear_usuario), name='crear_usuario'),
    path('usuarios/editar/<int:id>/', never_cache(views.editar_usuario), name='editar_usuario'),
    path('usuarios/eliminar/<int:id>/', never_cache(views.eliminar_usuario), name='eliminar_usuario'),

    # ============================================
    # PÁGINAS PÚBLICAS
    # ============================================
    path('', views.index, name='index'),
    path('sobre_nosotros/', views.sobre_nosotros, name='sobre_nosotros'),
    path('servicios/', views.servicios, name='servicios'),
    path('contactanos/', views.contactanos, name='contactanos'),

    # ============================================
    # MENÚ Y PEDIDOS (sin cache para datos actualizados)
    # ============================================
    path('menu/', never_cache(views.menu_view), name='menu'),
    path('confirmar_pedido/', never_cache(views.confirmar_pedido), name='confirmar_pedido'),
    
    # ============================================
    # COCINA - PEDIDOS (sin cache para tiempo real)
    # ============================================
    path('cocina/pedidos/', never_cache(views.cocina_pedidos), name='cocina_pedidos'),
    path('cocina/pedidos/<int:pedido_id>/cambiar_estado/', never_cache(views.cambiar_estado_pedido), name='cambiar_estado_pedido'),
    
    # ============================================
    # RUTAS DE PRUEBA PARA PÁGINAS DE ERROR
    # ⚠️ IMPORTANTE: Eliminar estas rutas en producción
    # ============================================
    path('test-404/', views.test_404, name='test_404'),
    path('test-500/', views.test_500, name='test_500'),
    path('test-403/', views.test_403, name='test_403'),
]
