# cocina/urls.py

from django.urls import path
from django.views.decorators.cache import never_cache
from . import views

app_name = 'cocina'

urlpatterns = [
    # ============================================
    # DASHBOARD DE COCINERO
    # ============================================
    path('dashboard/', never_cache(views.cocinero_dashboard), name='dashboard'),
    
    # ============================================
    # GESTIÓN DE PEDIDOS (sin cache para tiempo real)
    # ============================================
    path('pedidos/', never_cache(views.cocina_pedidos), name='pedidos'),
    path('pedidos/<int:pedido_id>/cambiar_estado/', never_cache(views.cambiar_estado_pedido), name='cambiar_estado_pedido'),
]