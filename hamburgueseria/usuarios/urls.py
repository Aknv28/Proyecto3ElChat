from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('cocinero_dashboard/', views.cocinero_dashboard, name='cocinero_dashboard'),
    path('cajero_dashboard/', views.cajero_dashboard, name='cajero_dashboard'),

    # Página principal (index)
    path('', views.index, name='index'),

    # Rutas adicionales para las secciones
    path('sobre_nosotros/', views.sobre_nosotros, name='sobre_nosotros'),
    path('servicios/', views.servicios, name='servicios'),
    path('contactanos/', views.contactanos, name='contactanos'),

    # Otras rutas
    path('menu/', views.menu_view, name='menu'),
    path('confirmar_pedido/', views.confirmar_pedido, name='confirmar_pedido'),
    path('cocina/pedidos/', views.cocina_pedidos, name='cocina_pedidos'),
    path('cocina/pedidos/<int:pedido_id>/cambiar_estado/', views.cambiar_estado_pedido, name='cambiar_estado_pedido'),
]
