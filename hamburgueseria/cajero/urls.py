# cajero/urls.py

from django.urls import path
from django.views.decorators.cache import never_cache
from . import views

app_name = 'cajero'

urlpatterns = [
    # ============================================
    # DASHBOARD DE CAJERO
    # ============================================
    path('dashboard/', never_cache(views.cajero_dashboard), name='dashboard'),
    
    # ============================================
    # MENÚ Y PEDIDOS (sin cache para datos actualizados)
    # ============================================
    path('menu/', never_cache(views.menu_view), name='menu'),
    path('confirmar_pedido/', never_cache(views.confirmar_pedido), name='confirmar_pedido'),

    # ============================================
    # PEDIDOS
    # ============================================
    path('pedidos/pendientes/', views.pedidos_pendientes, name='pedidos_pendientes'),
    
    # Cambiar a "en cocina"
    path('pedidos/<int:pedido_id>/a-cocina/', 
         views.cambiar_estado_a_cocina, 
         name='cambiar_estado'),
    
    # 👉 NUEVA RUTA PARA CANCELAR PEDIDO
    path('pedidos/<int:pedido_id>/cancelar/', 
         views.cancelar_pedido, 
         name='cancelar_pedido'),
]
