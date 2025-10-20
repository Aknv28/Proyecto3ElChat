from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from sistema.models import Producto, Categoria
import uuid
from django.utils import timezone
from sistema.models import Producto, Categoria, Pedido, PedidoDetalle
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

# Vista de login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            # Autenticación del usuario
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Verificar si las credenciales son correctas
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Verificar el rol del usuario
                if user.rol == 'admin':
                    login(request, user)
                    return redirect('admin_dashboard')
                elif user.rol == 'cocinero':
                    login(request, user)
                    return redirect('cocinero_dashboard')
                elif user.rol == 'cajero':
                    login(request, user)
                    return redirect('cajero_dashboard')
                else:
                    messages.error(request, 'No tienes permisos para acceder.')
                    return redirect('login')  # Redirige a login si no tiene rol válido
            else:
                messages.error(request, 'Credenciales incorrectas. Verifica tu usuario y contraseña.')

        else:
            messages.error(request, 'Credenciales incorrectas. Verifica tu usuario y contraseña.')

    else:
        form = AuthenticationForm()

    return render(request, 'usuarios/login.html', {'form': form})

# Vista para el dashboard del Admin
@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

# Vista para el dashboard del Cocinero
@login_required
def cocinero_dashboard(request):
    return render(request, 'cocinero_dashboard.html')

# Vista para el dashboard del Cajero
@login_required
def cajero_dashboard(request):
    return render(request, 'cajero_dashboard.html')

@login_required
def menu_view(request):
    categorias = Categoria.objects.all()
    productos_por_categoria = {
        c.nombre: Producto.objects.filter(categoria=c) for c in categorias
    }

    if request.method == 'POST':
        tipo = request.POST.get('tipo', 'local')  # 🍽️ Aquí por defecto
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

        return redirect('confirmar_pedido')

    # Recuperar pedido guardado si se está editando
    pedido_guardado = request.session.get('pedido', [])
    tipo_guardado = request.session.get('tipo', 'local')

    return render(request, 'usuarios/menu.html', {
        'productos_por_categoria': productos_por_categoria,
        'pedido_guardado': pedido_guardado,
        'tipo_guardado': tipo_guardado
    })

@login_required
def confirmar_pedido(request):
    pedido_sesion = request.session.get('pedido', [])
    total = request.session.get('total', 0)
    tipo = request.session.get('tipo', 'local')

    if not pedido_sesion:
        messages.info(request, "No hay productos en el pedido.")
        return redirect('menu')

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'cancelar':
            request.session.pop('pedido', None)
            request.session.pop('total', None)
            request.session.pop('tipo', None)
            messages.info(request, "Pedido cancelado.")
            return redirect('menu')

        elif action == 'editar':
            messages.info(request, "Puedes editar tu pedido.")
            return redirect('menu')

        elif action == 'mandar_a_cocina':
            cajero_actual = request.user

            pedido = Pedido.objects.create(
                cajero=cajero_actual,
                tipo=tipo,
                total_monetario=total,
                estado_actual='en_cocina'
            )

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

            messages.success(request, f"Pedido #{pedido.numero_pedido} enviado a cocina.")
            return redirect('menu')

    return render(request, 'usuarios/confirmar_pedido.html', {
        'pedido': pedido_sesion,
        'total': total,
        'tipo': tipo
    })

@login_required
def cocina_pedidos(request):
    # Obtener todos los pedidos con estado "en_cocina"
    pedidos = Pedido.objects.filter(estado_actual='en_cocina').order_by('creado_en')
    
    return render(request, 'cocina/pedidos_en_cocina.html', {'pedidos': pedidos})

@login_required
def cambiar_estado_pedido(request, pedido_id):
    # Cambiar el estado del pedido de "en_cocina" a "listo"
    pedido = Pedido.objects.get(id=pedido_id)
    if pedido.estado_actual == 'en_cocina':
        pedido.estado_actual = 'listo'
        pedido.save()
    return redirect('cocina_pedidos')  # Redirige nuevamente a la lista de pedidos


def index(request):
    return render(request, 'usuarios/index.html')

def index(request):
    return render(request, 'usuarios/index.html')

def sobre_nosotros(request):
    return render(request, 'usuarios/sobre_nosotros.html')

def servicios(request):
    return render(request, 'usuarios/servicios.html')

def contactanos(request):
    return render(request, 'usuarios/contactanos.html')