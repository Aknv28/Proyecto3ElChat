from rest_framework import serializers
from .models import Producto, Cliente, Pedido, PedidoDetalle

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'imagen_url', 'categoria']

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'email', 'telefono']

class PedidoDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedidoDetalle
        fields = ['producto', 'cantidad', 'precio_unitario', 'subtotal']

class PedidoSerializer(serializers.ModelSerializer):
    detalles = PedidoDetalleSerializer(many=True, write_only=True)
    
    class Meta:
        model = Pedido
        fields = ['numero_pedido', 'tipo', 'estado_actual', 'total_monetario', 
                  'cliente', 'cajero', 'detalles']
        read_only_fields = ['numero_pedido']
