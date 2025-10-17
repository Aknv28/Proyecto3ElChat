from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('cocinero_dashboard/', views.cocinero_dashboard, name='cocinero_dashboard'),
    path('cajero_dashboard/', views.cajero_dashboard, name='cajero_dashboard'),



    path('menu/', views.menu_view, name='menu'),
    path('confirmar_pedido/', views.confirmar_pedido, name='confirmar_pedido'),


    path('cocina/pedidos/', views.cocina_pedidos, name='cocina_pedidos'),
    path('cocina/pedidos/<int:pedido_id>/cambiar_estado/', views.cambiar_estado_pedido, name='cambiar_estado_pedido'),

]
