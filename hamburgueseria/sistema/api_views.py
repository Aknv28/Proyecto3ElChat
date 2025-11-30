from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Producto, Cliente, Pedido, PedidoDetalle
from .serializers import ProductoSerializer, ClienteSerializer, PedidoSerializer
import uuid

@api_view(['GET'])
def productos_por_categoria(request, categoria_id):
    """Obtener productos por categoría"""
    productos = Producto.objects.filter(categoria_id=categoria_id, activo=True)
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def crear_pedido_completo(request):
    """
    Crear pedido completo con cliente y detalles
    
    Body esperado:
    {
        "cliente": {
            "nombre": "Juan Pérez",
            "ci": "12345678",
            "telefono": "+59171914583"
        },
        "cajero_id": 3,
        "total": 105.50,
        "detalles": [
            {
                "producto_id": 25,
                "cantidad": 2,
                "precio_unitario": 35.00,
                "subtotal": 70.00
            },
            {
                "producto_id": 26,
                "cantidad": 1,
                "precio_unitario": 40.00,
                "subtotal": 40.00
            }
        ]
    }
    """
    try:
        # 1. Crear o obtener cliente
        cliente_data = request.data.get('cliente')
        cliente, created = Cliente.objects.get_or_create(
            email=f"{cliente_data['ci']}@temp.com",
            defaults={
                'nombre': cliente_data['nombre'],
                'telefono': cliente_data.get('telefono', '+59171914583')
            }
        )
        
        # 2. Crear pedido
        cajero_id = request.data.get('cajero_id', 3)  # Por defecto cajero con id=3
        total = request.data.get('total')
        
        from usuarios.models import Usuario
        cajero = get_object_or_404(Usuario, id=cajero_id)
        
        pedido = Pedido.objects.create(
            numero_pedido=str(uuid.uuid4()),
            tipo='llevar',
            estado_actual='pendiente',
            total_monetario=total,
            cliente=cliente,
            cajero=cajero,
            prioridad=0,
            tiempo_espera=0,
            tiempo_estimado_total=0
        )
        
        # 3. Crear detalles del pedido
        detalles_data = request.data.get('detalles', [])
        for detalle in detalles_data:
            producto = get_object_or_404(Producto, id=detalle['producto_id'])
            PedidoDetalle.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=detalle['cantidad'],
                precio_unitario=detalle['precio_unitario'],
                subtotal=detalle['subtotal']
            )
        
        return Response({
            'success': True,
            'numero_pedido': pedido.numero_pedido,
            'cliente_id': cliente.id,
            'mensaje': 'Pedido creado exitosamente'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)