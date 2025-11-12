# cocina/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from sistema.models import Pedido

# ============================================
# DASHBOARD DE COCINERO
# ============================================

@login_required
@never_cache
def cocinero_dashboard(request):
    """Dashboard principal del cocinero"""
    # Verificar que el usuario es cocinero
    if request.user.rol != 'cocinero':
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('usuarios:login')
    
    # Limpiar mensajes anteriores que no deberían estar aquí
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
    """Lista de pedidos en cocina para preparar"""
    # Verificar que el usuario es cocinero
    if request.user.rol != 'cocinero':
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('usuarios:login')
    
    # Obtener todos los pedidos con estado "en_cocina"
    pedidos = Pedido.objects.filter(estado_actual='en_cocina').order_by('creado_en')
    
    return render(request, 'cocina/pedidos_en_cocina.html', {'pedidos': pedidos})


@login_required
@never_cache
def cambiar_estado_pedido(request, pedido_id):
    """Cambia el estado de un pedido de 'en_cocina' a 'listo'"""
    # Verificar que el usuario es cocinero
    if request.user.rol != 'cocinero':
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('usuarios:login')
    
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=pedido_id)
        
        if pedido.estado_actual == 'en_cocina':
            pedido.estado_actual = 'listo'
            pedido.save()
            messages.success(request, f'✅ Pedido #{pedido.numero_pedido} marcado como listo.')
        else:
            messages.warning(request, f'⚠️ El pedido #{pedido.numero_pedido} ya no está en cocina.')
        
        return redirect('cocina:pedidos')
    
    # Si no es POST, redirigir a la lista de pedidos
    return redirect('cocina:pedidos')