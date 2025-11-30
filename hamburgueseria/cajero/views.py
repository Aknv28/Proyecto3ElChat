# cajero/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.http import JsonResponse
from sistema.models import Producto, Categoria, Pedido, PedidoDetalle

# ============================================
# DASHBOARD DE CAJERO
# ============================================

@login_required
@never_cache
def cajero_dashboard(request):
    """Dashboard principal del cajero"""
    # Verificar que el usuario es cajero
    if request.user.rol != 'cajero':
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('usuarios:login')
    
    # Limpiar mensajes anteriores que no deberían estar aquí
    storage = messages.get_messages(request)
    storage.used = True
    
    return render(request, 'cajero/cajero_dashboard.html', {
        'usuario': request.user
    })


# ============================================
# MENÚ Y GESTIÓN DE PEDIDOS
# ============================================

@login_required
@never_cache
def menu_view(request):
    """Vista del menú para realizar pedidos"""
    # Verificar que el usuario es cajero
    if request.user.rol != 'cajero':
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('usuarios:login')
    
    categorias = Categoria.objects.all()
    productos_por_categoria = {
        c.nombre: Producto.objects.filter(categoria=c) for c in categorias
    }

    if request.method == 'POST':
        tipo = request.POST.get('tipo', 'local')  # 🍽️ Por defecto local
        pedido = []
        total = 0

        for categoria, productos in productos_por_categoria.items():
            for producto in productos:
                cantidad = int(request.POST.get(f'producto_{producto.id}') or 0)
                if cantidad > 0:
                    subtotal = producto.precio * cantidad
                    pedido.append({
                        'id': producto.id,
                        'nombre': producto.nombre,
                        'cantidad': cantidad,
                        'precio': float(producto.precio),
                        'subtotal': float(subtotal)
                    })
                    total += subtotal

        # Guardar en sesión
        request.session['pedido'] = pedido
        request.session['total'] = float(total)
        request.session['tipo'] = tipo

        return redirect('cajero:confirmar_pedido')

    # Recuperar pedido guardado si se está editando
    pedido_guardado = request.session.get('pedido', [])
    tipo_guardado = request.session.get('tipo', 'local')

    return render(request, 'cajero/menu.html', {
        'productos_por_categoria': productos_por_categoria,
        'pedido_guardado': pedido_guardado,
        'tipo_guardado': tipo_guardado
    })


@login_required
@never_cache
def confirmar_pedido(request):
    """Confirma y procesa el pedido realizado"""
    # Verificar que el usuario es cajero
    if request.user.rol != 'cajero':
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('usuarios:login')
    
    pedido_sesion = request.session.get('pedido', [])
    total = request.session.get('total', 0)
    tipo = request.session.get('tipo', 'local')

    if not pedido_sesion:
        messages.info(request, "No hay productos en el pedido.")
        return redirect('cajero:menu')

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'cancelar':
            # Cancelar pedido
            request.session.pop('pedido', None)
            request.session.pop('total', None)
            request.session.pop('tipo', None)
            messages.info(request, "Pedido cancelado.")
            return redirect('cajero:menu')

        elif action == 'editar':
            # Volver a editar
            messages.info(request, "Puedes editar tu pedido.")
            return redirect('cajero:menu')

        elif action == 'mandar_a_cocina':
            try:
                cajero_actual = request.user

                # Crear el pedido en la base de datos
                pedido = Pedido.objects.create(
                    cajero=cajero_actual,
                    tipo=tipo,
                    total_monetario=total,
                    estado_actual='en_cocina'
                )

                # Crear los detalles del pedido
                for item in pedido_sesion:
                    producto = Producto.objects.get(id=item['id'])
                    PedidoDetalle.objects.create(
                        pedido=pedido,
                        producto=producto,
                        cantidad=item['cantidad'],
                        precio_unitario=item['precio'],
                        subtotal=item['subtotal']
                    )

                # Limpiar sesión
                request.session.pop('pedido', None)
                request.session.pop('total', None)
                request.session.pop('tipo', None)

                # Mensaje de éxito
                messages.success(request, f"Pedido #{pedido.numero_pedido} enviado a cocina exitosamente.")
                
                # Si es una petición AJAX, devolver JSON
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'numero_pedido': pedido.numero_pedido
                    })
                
                return redirect('cajero:menu')
                
            except Exception as e:
                messages.error(request, f"Error al procesar el pedido: {str(e)}")
                
                # Si es una petición AJAX, devolver error
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'error': str(e)
                    }, status=500)
                
                return redirect('cajero:confirmar_pedido')

    return render(request, 'cajero/confirmar_pedido.html', {
        'pedido': pedido_sesion,
        'total': total,
        'tipo': tipo
    })

@login_required
@never_cache
def pedidos_pendientes(request):
    """Lista todos los pedidos con estado pendiente para el cajero"""

    # Verificar que el usuario es cajero
    if request.user.rol != 'cajero':
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('usuarios:login')

    pedidos = Pedido.objects.filter(estado_actual='pendiente').order_by('creado_en')

    return render(request, 'cajero/pedidos_pendientes.html', {
        'pedidos': pedidos
    })

from django.shortcuts import get_object_or_404, redirect
from sistema.models import Pedido

from django.utils import timezone

def cambiar_estado_a_cocina(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    # Cambiar estado a EN COCINA
    pedido.estado_actual = 'en_cocina'

# Reiniciar tiempo de espera
    pedido.creado_en = timezone.now()  # Aquí se actualiza la fecha/hora
    pedido.tiempo_espera = 0  # Si tienes un campo explícito

    pedido.save()

    return redirect('cajero:pedidos_pendientes')

def cancelar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.estado_actual = "cancelado"
    pedido.save()
    return redirect('cajero:pedidos_pendientes')