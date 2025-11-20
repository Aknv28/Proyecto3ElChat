# cocina/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from datetime import datetime
from sistema.models import Pedido

# ============================================
# DASHBOARD DE COCINERO
# ============================================

@login_required
@never_cache
def cocinero_dashboard(request):
    """Dashboard principal del cocinero"""
    if request.user.rol != 'cocinero':
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('usuarios:login')

    storage = messages.get_messages(request)
    storage.used = True
    
    return render(request, 'cocina/cocinero_dashboard.html', {
        'usuario': request.user
    })


# ============================================
# GESTIÓN DE PEDIDOS EN COCINA
# ============================================

@login_required
@never_cache
def cocina_pedidos(request):
    """Lista de pedidos ordenados por prioridad según teoría de colas M/M/1"""
    if request.user.rol != 'cocinero':
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('usuarios:login')
    
    # Obtener pedidos que están pendientes o en cocina
    pedidos = Pedido.objects.filter(
        estado_actual__in=['pendiente', 'en_cocina']
    )

    # Recalcular prioridad para cada pedido
    for pedido in pedidos:
        pedido.calcular_tiempo_estimado()
        pedido.calcular_prioridad(alpha=0.05)
        pedido.save()

    # Ordenar por prioridad (mayor primero)
    pedidos_ordenados = sorted(pedidos, key=lambda x: x.prioridad, reverse=True)

    return render(request, 'cocina/pedidos_en_cocina.html', {
        'pedidos': pedidos_ordenados
    })


# ============================================
# CAMBIAR ESTADO DE PEDIDO
# ============================================

@login_required
@never_cache
def cambiar_estado_pedido(request, pedido_id):
    """Cambia el estado de un pedido de 'en_cocina' a 'listo'"""
    if request.user.rol != 'cocinero':
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('usuarios:login')
    
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=pedido_id)
        
        if pedido.estado_actual in ['pendiente', 'en_cocina']:
            pedido.estado_actual = 'listo'
            pedido.save()
            messages.success(request, f'✅ Pedido #{pedido.numero_pedido} marcado como listo.')
        else:
            messages.warning(request, f'⚠️ El pedido #{pedido.numero_pedido} ya no está disponible para cambiar estado.')
        
        return redirect('cocina:pedidos')
    
    return redirect('cocina:pedidos')




from django.http import JsonResponse

@login_required
@never_cache
def pedidos_json(request):
    """Devuelve los pedidos actualizados como JSON (para refrescar dinámicamente la vista)"""
    if request.user.rol != 'cocinero':
        return JsonResponse({'error': 'No autorizado'}, status=403)

    pedidos = Pedido.objects.filter(
        estado_actual__in=['pendiente', 'en_cocina']
    )

    # recalcular prioridad antes de enviar
    data = []
    for p in pedidos:
        p.calcular_tiempo_estimado()
        p.calcular_prioridad()
        p.save()
        data.append({
            'id': p.id,
            'numero_pedido': str(p.numero_pedido),
            'tipo': p.tipo,
            'total_monetario': float(p.total_monetario),
            'prioridad': round(p.prioridad, 2),
            'tiempo_espera': round(p.tiempo_espera, 1),
            'tiempo_estimado_total': round(p.tiempo_estimado_total, 1),
            'cantidad_hamburguesas': p.cantidad_hamburguesas(),
            'estado': p.estado_actual,
            'detalles': [
                {
                    'producto': d.producto.nombre,
                    'cantidad': d.cantidad,
                    'precio_unitario': float(d.precio_unitario)
                } for d in p.detalles.all()
            ]
        })

    # ordenar de mayor a menor prioridad
    data.sort(key=lambda x: x['prioridad'], reverse=True)

    return JsonResponse({'pedidos': data})
