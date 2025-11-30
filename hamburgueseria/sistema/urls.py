from django.urls import path
from . import api_views

urlpatterns = [
    # ... tus otras URLs ...
    
    # APIs para Flutter
    path('api/productos/categoria/<int:categoria_id>/', 
         api_views.productos_por_categoria, 
         name='api_productos_categoria'),
    path('api/pedido/crear/', 
         api_views.crear_pedido_completo, 
         name='api_crear_pedido'),
]