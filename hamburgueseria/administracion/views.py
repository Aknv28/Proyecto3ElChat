# administracion/views.py
import json
from django.template.response import TemplateResponse
from django.db.models import Sum, Count
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta

from .models import Categoria, Pedido
from usuarios.models import Usuario  # Importar modelo Usuario

# ============================================
# DASHBOARD DE ADMINISTRADOR
# ============================================

@login_required
@never_cache
def admin_dashboard(request):
    """Dashboard principal del administrador con estadísticas en tiempo real"""
    if getattr(request.user, 'rol', '') != 'admin':
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('usuarios:login')

    # Limpiar mensajes anteriores
    storage = messages.get_messages(request)
    storage.used = True

    # ═══════════════════════════════════════════
    # ESTADÍSTICA 1: Total de usuarios
    # ═══════════════════════════════════════════
    total_usuarios = Usuario.objects.count()

    # ═══════════════════════════════════════════
    # ESTADÍSTICA 2: Pedidos de hoy
    # ═══════════════════════════════════════════
    hoy = timezone.now().date()
    inicio_dia = datetime.combine(hoy, datetime.min.time())
    fin_dia = datetime.combine(hoy, datetime.max.time())
    
    # Hacer timezone-aware si estás usando timezone
    if timezone.is_aware(timezone.now()):
        inicio_dia = timezone.make_aware(inicio_dia)
        fin_dia = timezone.make_aware(fin_dia)
    
    pedidos_hoy = Pedido.objects.filter(
        creado_en__range=(inicio_dia, fin_dia)
    ).count()

    # ═══════════════════════════════════════════
    # ESTADÍSTICA 3: Pedidos en cocina
    # ═══════════════════════════════════════════
    pedidos_en_cocina = Pedido.objects.filter(
        estado_actual='en_cocina'
    ).count()

    # ═══════════════════════════════════════════
    # ESTADÍSTICAS ADICIONALES (opcionales)
    # ═══════════════════════════════════════════
    # Pedidos pendientes
    pedidos_pendientes = Pedido.objects.filter(
        estado_actual='pendiente'
    ).count()

    # Pedidos listos
    pedidos_listos = Pedido.objects.filter(
        estado_actual='listo'
    ).count()

    # Total de ventas del día
    ventas_hoy = Pedido.objects.filter(
        creado_en__range=(inicio_dia, fin_dia)
    ).aggregate(total=Sum('total_monetario'))['total'] or 0

    # Pedidos entregados hoy
    pedidos_entregados_hoy = Pedido.objects.filter(
        creado_en__range=(inicio_dia, fin_dia),
        estado_actual='entregado'
    ).count()

    contexto = {
        'usuario': request.user,
        'total_usuarios': total_usuarios,
        'pedidos_hoy': pedidos_hoy,
        'pedidos_en_cocina': pedidos_en_cocina,
        # Estadísticas adicionales
        'pedidos_pendientes': pedidos_pendientes,
        'pedidos_listos': pedidos_listos,
        'ventas_hoy': round(ventas_hoy, 2),
        'pedidos_entregados_hoy': pedidos_entregados_hoy,
    }

    return render(request, 'administracion/admin_dashboard.html', contexto)


# ============================================
# VISTA DETALLADA: USUARIOS
# ============================================

@login_required
@never_cache
def detalle_usuarios(request):
    """Vista detallada de usuarios del sistema"""
    if getattr(request.user, 'rol', '') != 'admin':
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('usuarios:login')

    # Obtener todos los usuarios con estadísticas
    usuarios = Usuario.objects.annotate(
        pedidos_realizados=Count('pedido', distinct=True)
    ).order_by('-date_joined')

    # Estadísticas por rol
    usuarios_por_rol = Usuario.objects.values('rol').annotate(
        total=Count('id')
    ).order_by('-total')

    # Usuarios activos (que han iniciado sesión recientemente)
    hace_30_dias = timezone.now() - timedelta(days=30)
    usuarios_activos = Usuario.objects.filter(
        last_login__gte=hace_30_dias
    ).count()

    contexto = {
        'usuarios': usuarios,
        'total_usuarios': usuarios.count(),
        'usuarios_por_rol': usuarios_por_rol,
        'usuarios_activos': usuarios_activos,
    }

    return render(request, 'administracion/detalle_usuarios.html', contexto)


# ============================================
# VISTA DETALLADA: PEDIDOS DE HOY
# ============================================

@login_required
@never_cache
def detalle_pedidos_hoy(request):
    """Vista detallada de pedidos del día actual"""
    if getattr(request.user, 'rol', '') != 'admin':
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('usuarios:login')

    # Obtener fecha de hoy
    hoy = timezone.now().date()
    inicio_dia = datetime.combine(hoy, datetime.min.time())
    fin_dia = datetime.combine(hoy, datetime.max.time())
    
    if timezone.is_aware(timezone.now()):
        inicio_dia = timezone.make_aware(inicio_dia)
        fin_dia = timezone.make_aware(fin_dia)

    # Pedidos de hoy
    pedidos_hoy = Pedido.objects.filter(
        creado_en__range=(inicio_dia, fin_dia)
    ).select_related('cliente', 'cajero').order_by('-creado_en')

    # Estadísticas del día
    total_ventas_hoy = pedidos_hoy.aggregate(
        total=Sum('total_monetario')
    )['total'] or 0

    pedidos_por_estado = pedidos_hoy.values('estado_actual').annotate(
        total=Count('id')
    )

    pedidos_por_tipo = pedidos_hoy.values('tipo').annotate(
        total=Count('id')
    )

    # Hora pico (hora con más pedidos)
    pedidos_por_hora = pedidos_hoy.extra(
        select={'hora': 'EXTRACT(hour FROM creado_en)'}
    ).values('hora').annotate(total=Count('id')).order_by('-total')

    contexto = {
        'pedidos': pedidos_hoy,
        'total_pedidos': pedidos_hoy.count(),
        'total_ventas': round(total_ventas_hoy, 2),
        'pedidos_por_estado': pedidos_por_estado,
        'pedidos_por_tipo': pedidos_por_tipo,
        'hora_pico': pedidos_por_hora.first() if pedidos_por_hora else None,
    }

    return render(request, 'administracion/detalle_pedidos_hoy.html', contexto)


# ============================================
# VISTA DETALLADA: PEDIDOS EN COCINA
# ============================================

@login_required
@never_cache
def detalle_pedidos_cocina(request):
    """Vista detallada de pedidos actualmente en cocina"""
    if getattr(request.user, 'rol', '') != 'admin':
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('usuarios:login')

    # Pedidos en cocina ordenados por prioridad
    pedidos_cocina = Pedido.objects.filter(
        estado_actual='en_cocina'
    ).select_related('cliente', 'cajero').prefetch_related(
        'detalles__producto'
    ).order_by('-prioridad', 'creado_en')

    # Calcular tiempos
    for pedido in pedidos_cocina:
        tiempo_transcurrido = (timezone.now() - pedido.creado_en).total_seconds() / 60
        pedido.tiempo_transcurrido = round(tiempo_transcurrido, 1)
        pedido.porcentaje_completado = min(
            100, 
            (tiempo_transcurrido / pedido.tiempo_estimado_total * 100) if pedido.tiempo_estimado_total > 0 else 0
        )

    # Estadísticas de cocina
    total_hamburguesas = sum(
        pedido.cantidad_hamburguesas() for pedido in pedidos_cocina
    )

    tiempo_promedio_espera = pedidos_cocina.aggregate(
        promedio=Sum('tiempo_espera')
    )['promedio'] or 0
    
    if pedidos_cocina.count() > 0:
        tiempo_promedio_espera = tiempo_promedio_espera / pedidos_cocina.count()

    # Pedido más antiguo
    pedido_mas_antiguo = pedidos_cocina.order_by('creado_en').first()

    contexto = {
        'pedidos': pedidos_cocina,
        'total_pedidos': pedidos_cocina.count(),
        'total_hamburguesas': total_hamburguesas,
        'tiempo_promedio_espera': round(tiempo_promedio_espera, 1),
        'pedido_mas_antiguo': pedido_mas_antiguo,
    }

    return render(request, 'administracion/detalle_pedidos_cocina.html', contexto)


# ============================================
# VISTA DE REPORTES (existente, mejorada)
# ============================================

@login_required
@never_cache
def reportes_dashboard(request):
    """Vista de reportes con gráficos de ventas y pedidos"""
    if getattr(request.user, 'rol', '') != 'admin':
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('usuarios:login')

    # Ventas por categoría
    categorias = list(Categoria.objects.values_list('nombre', flat=True))
    totales = list(
        Categoria.objects.annotate(
            total_ventas=Sum('producto__pedidodetalle__subtotal')
        ).values_list('total_ventas', flat=True)
    )

    # Pedidos por estado
    estados = [estado[1] for estado in Pedido.ESTADO_CHOICES]
    totales_estados = []
    for estado in [estado[0] for estado in Pedido.ESTADO_CHOICES]:
        count = Pedido.objects.filter(estado_actual=estado).count()
        totales_estados.append(count)

    # Ventas de los últimos 7 días
    hoy = timezone.now().date()
    hace_7_dias = hoy - timedelta(days=7)
    
    ventas_semana = []
    fechas_semana = []
    
    for i in range(7):
        fecha = hace_7_dias + timedelta(days=i)
        inicio = datetime.combine(fecha, datetime.min.time())
        fin = datetime.combine(fecha, datetime.max.time())
        
        if timezone.is_aware(timezone.now()):
            inicio = timezone.make_aware(inicio)
            fin = timezone.make_aware(fin)
        
        total = Pedido.objects.filter(
            creado_en__range=(inicio, fin)
        ).aggregate(total=Sum('total_monetario'))['total'] or 0
        
        ventas_semana.append(float(total))
        fechas_semana.append(fecha.strftime('%d/%m'))

    contexto = {
        "titulo": "Panel de Reportes",
        "categorias": json.dumps(categorias),
        "totales": json.dumps([float(t) if t else 0 for t in totales]),
        "estados": json.dumps(estados),
        "totales_estados": json.dumps(totales_estados),
        "fechas_semana": json.dumps(fechas_semana),
        "ventas_semana": json.dumps(ventas_semana),
    }

    return TemplateResponse(request, "administracion/reportes_dashboard.html", contexto)

