# cocina/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.http import JsonResponse
from sistema.models import Pedido


def permitir_cocina(user):
    """Verifica si el usuario tiene permiso para acceder a cocina"""
    return user.rol in ['cocinero', 'admin']


@login_required
@never_cache
def cocinero_dashboard(request):
    """Dashboard principal del cocinero o admin"""
    if not permitir_cocina(request.user):
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('usuarios:login')

    storage = messages.get_messages(request)
    storage.used = True
    
    return render(request, 'cocina/cocinero_dashboard.html', {
        'usuario': request.user
    })


@login_required
@never_cache
def cocina_pedidos(request):
    """
    📋 LISTA DE PEDIDOS ORDENADOS POR PRIORIDAD
    
    🔥 REGLA PRINCIPAL:
    - El PRIMER pedido está FIJO (en_preparacion=True)
    - Los demás se ordenan dinámicamente por prioridad
    - Cuando el primero se marca como "listo", el segundo sube automáticamente
    """
    
    if not permitir_cocina(request.user):
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('usuarios:login')
    
    # Obtener todos los pedidos en cocina
    pedidos = Pedido.objects.filter(estado_actual='en_cocina')

    # ════════════════════════════════════════════════════════
    # PASO 1: Identificar o establecer el pedido en preparación
    # ════════════════════════════════════════════════════════
    pedido_en_preparacion = pedidos.filter(en_preparacion=True).first()
    
    # Si no hay ninguno marcado, marcar el más antiguo
    if not pedido_en_preparacion and pedidos.exists():
        pedido_mas_antiguo = pedidos.order_by('creado_en').first()
        pedido_mas_antiguo.en_preparacion = True
        pedido_mas_antiguo.save()
        pedido_en_preparacion = pedido_mas_antiguo

    # ════════════════════════════════════════════════════════
    # PASO 2: Obtener el resto de pedidos (sin el que está fijo)
    # ════════════════════════════════════════════════════════
    otros_pedidos = pedidos.exclude(id=pedido_en_preparacion.id) if pedido_en_preparacion else pedidos

    # ════════════════════════════════════════════════════════
    # PASO 3: Calcular prioridades para los otros pedidos
    # ════════════════════════════════════════════════════════
    pedidos_con_prioridad = []
    for pedido in otros_pedidos:
        pedido.calcular_tiempo_estimado()
        pedido.calcular_prioridad(
            peso_tiempo=0.35,      # 35% tiempo de espera
            peso_tipo=0.25,        # 25% tipo de pedido (llevar vs local)
            peso_eficiencia=0.25,  # 25% balance cantidad/tiempo
            peso_urgencia=0.15     # 15% urgencia por retraso
        )
        pedido.save()
        pedidos_con_prioridad.append(pedido)

    # ════════════════════════════════════════════════════════
    # PASO 4: Ordenar por prioridad (mayor a menor)
    # ════════════════════════════════════════════════════════
    pedidos_ordenados = sorted(pedidos_con_prioridad, key=lambda x: x.prioridad, reverse=True)

    # ════════════════════════════════════════════════════════
    # PASO 5: Construir lista final (primero el fijo, luego ordenados)
    # ════════════════════════════════════════════════════════
    lista_final = []
    
    if pedido_en_preparacion:
        # Actualizar info del pedido fijo
        pedido_en_preparacion.calcular_tiempo_estimado()
        pedido_en_preparacion.calcular_prioridad()  # Esto le asigna prioridad = 999
        pedido_en_preparacion.save()
        lista_final.append(pedido_en_preparacion)
    
    lista_final.extend(pedidos_ordenados)

    return render(request, 'cocina/pedidos_en_cocina.html', {
        'pedidos': lista_final,
        'pedido_fijo': pedido_en_preparacion  # Para usar en el template si es necesario
    })


@login_required
@never_cache
def cambiar_estado_pedido(request, pedido_id):
    """
    🔄 CAMBIAR ESTADO DE PEDIDO: en_cocina → listo
    
    🔥 LÓGICA ESPECIAL:
    Si el pedido marcado como "listo" es el que estaba en preparación:
    1. Se quita la marca en_preparacion
    2. Se busca el siguiente pedido con mayor prioridad
    3. Se le asigna en_preparacion=True (sube a posición 1)
    """
    if not permitir_cocina(request.user):
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('usuarios:login')
    
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=pedido_id)
        
        if pedido.estado_actual == 'en_cocina':
            
            # ════════════════════════════════════════════════════════
            # Si era el pedido en preparación, promover al siguiente
            # ════════════════════════════════════════════════════════
            if pedido.en_preparacion:
                pedido.en_preparacion = False
                
                # Obtener otros pedidos en cocina
                otros_pedidos = Pedido.objects.filter(
                    estado_actual='en_cocina',
                    en_preparacion=False
                ).exclude(id=pedido.id)
                
                if otros_pedidos.exists():
                    # Recalcular prioridades
                    pedidos_list = []
                    for p in otros_pedidos:
                        p.calcular_tiempo_estimado()
                        p.calcular_prioridad(
                            peso_tiempo=0.35,
                            peso_tipo=0.25,
                            peso_eficiencia=0.25,
                            peso_urgencia=0.15
                        )
                        p.save()
                        pedidos_list.append(p)
                    
                    # El de mayor prioridad sube a posición 1
                    siguiente = max(pedidos_list, key=lambda x: x.prioridad)
                    siguiente.en_preparacion = True
                    siguiente.save()
                    
                    messages.info(request, f'🔄 Pedido #{siguiente.numero_pedido} ahora en preparación.')
            
            # Marcar como listo
            pedido.estado_actual = 'listo'
            pedido.save()
            messages.success(request, f'✅ Pedido #{pedido.numero_pedido} marcado como listo.')
            
        else:
            messages.warning(request, f'⚠️ El pedido #{pedido.numero_pedido} ya no está en cocina.')
        
        return redirect('cocina:pedidos')
    
    return redirect('cocina:pedidos')


@login_required
@never_cache
def pedidos_json(request):
    """
    📊 API JSON para actualización automática
    Devuelve los pedidos actualizados en formato JSON
    """
    
    if not permitir_cocina(request.user):
        return JsonResponse({'error': 'No autorizado'}, status=403)

    pedidos = Pedido.objects.filter(estado_actual='en_cocina')
    
    # Identificar pedido fijo
    pedido_fijo = pedidos.filter(en_preparacion=True).first()
    otros = pedidos.exclude(id=pedido_fijo.id) if pedido_fijo else pedidos

    data = []
    
    # Procesar pedido fijo
    if pedido_fijo:
        pedido_fijo.calcular_tiempo_estimado()
        pedido_fijo.calcular_prioridad()
        pedido_fijo.save()
        data.append(_pedido_to_dict(pedido_fijo, es_fijo=True))
    
    # Procesar otros pedidos
    otros_list = []
    for p in otros:
        p.calcular_tiempo_estimado()
        p.calcular_prioridad(
            peso_tiempo=0.35,
            peso_tipo=0.25,
            peso_eficiencia=0.25,
            peso_urgencia=0.15
        )
        p.save()
        otros_list.append(p)
    
    # Ordenar otros por prioridad
    otros_ordenados = sorted(otros_list, key=lambda x: x.prioridad, reverse=True)
    
    for p in otros_ordenados:
        data.append(_pedido_to_dict(p, es_fijo=False))

    return JsonResponse({'pedidos': data})


def _pedido_to_dict(pedido, es_fijo=False):
    """
    Helper: Convierte un pedido a diccionario para JSON
    """
    return {
        'id': pedido.id,
        'numero_pedido': str(pedido.numero_pedido),
        'tipo': pedido.tipo,
        'total_monetario': float(pedido.total_monetario),
        'prioridad': round(pedido.prioridad, 2),
        'tiempo_espera': round(pedido.tiempo_espera, 1),
        'tiempo_estimado_total': round(pedido.tiempo_estimado_total, 1),
        'cantidad_hamburguesas': pedido.cantidad_hamburguesas(),
        'estado': pedido.estado_actual,
        'en_preparacion': es_fijo,
        'detalles': [
            {
                'producto': d.producto.nombre,
                'cantidad': d.cantidad,
                'precio_unitario': float(d.precio_unitario)
            } for d in pedido.detalles.all()
        ]
    }