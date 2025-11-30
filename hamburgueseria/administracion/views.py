# administracion/views.py
import json
from django.template.response import TemplateResponse
from django.db.models import Sum, Count
from .models import Categoria, Pedido

# ============================================
# DASHBOARD DE ADMINISTRADOR
# ============================================
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages

@login_required
@never_cache
def admin_dashboard(request):
    """Dashboard principal del administrador"""
    if getattr(request.user, 'rol', '') != 'admin':
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('usuarios:login')

    # Limpiar mensajes anteriores
    storage = messages.get_messages(request)
    storage.used = True

    return render(request, 'administracion/admin_dashboard.html', {
        'usuario': request.user
    })

# ============================================
# VISTA DE REPORTES
# ============================================

@login_required
@never_cache
def reportes_dashboard(request):
    """Vista de reportes con gráficos de ventas y pedidos"""
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

    contexto = {
        "titulo": "Panel de Reportes",
        "categorias": json.dumps(categorias),
        "totales": json.dumps([t or 0 for t in totales]),  # reemplazar None por 0
        "estados": json.dumps(estados),
        "totales_estados": json.dumps(totales_estados),
    }

    return TemplateResponse(request, "administracion/reportes_dashboard.html", contexto)
