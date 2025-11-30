import json
from django.template.response import TemplateResponse   # También corrijo esto, usaste SimpleTemplateResponse arriba
from django.db import models
from sistema.models import Producto, Categoria, Pedido, PedidoDetalle

def reportes_dashboard(request):
    # -----------------------------
    # Ventas por categoría
    # -----------------------------
    categorias = []
    totales = []

    for categoria in Categoria.objects.all():
        categorias.append(categoria.nombre)

        total_categoria = PedidoDetalle.objects.filter(
            producto__categoria=categoria
        ).aggregate(total=models.Sum('subtotal'))['total'] or 0

        totales.append(float(total_categoria))

    # -----------------------------
    # Pedidos por estado
    # -----------------------------
    estados = list(Pedido.objects.values_list('estado_actual', flat=True).distinct())
    totales_estados = []

    for estado in estados:
        count = Pedido.objects.filter(estado_actual=estado).count()
        totales_estados.append(count)

    # -----------------------------
    # Contexto para el template
    # -----------------------------
    contexto = {
        "titulo": "Panel de Reportes",
        "categorias": json.dumps(categorias),
        "totales": json.dumps(totales),
        "estados": json.dumps(estados),
        "totales_estados": json.dumps(totales_estados),
    }

    return TemplateResponse(request, "administracion/reportes_dashboard.html", contexto)
