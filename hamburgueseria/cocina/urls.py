# cocina/urls.py

from django.urls import path
from django.views.decorators.cache import never_cache
from . import views

app_name = 'cocina'

urlpatterns = [
    # ============================================
    # DASHBOARD DEL COCINERO
    # ============================================
    path('dashboard/', never_cache(views.cocinero_dashboard), name='dashboard'),

    # ============================================
    # GESTIÓN DE PEDIDOS EN COCINA (VISTA PRINCIPAL)
    # ============================================
    path('pedidos/', never_cache(views.cocina_pedidos), name='pedidos'),

    # Cambiar estado del pedido (en cocina → listo)
    path('pedidos/<int:pedido_id>/cambiar_estado/', never_cache(views.cambiar_estado_pedido), name='cambiar_estado_pedido'),

    # ============================================
    # API JSON PARA REFRESCO AUTOMÁTICO (AJAX)
    # ============================================
    path('api/pedidos-json/', never_cache(views.pedidos_json), name='pedidos_json'),
]
