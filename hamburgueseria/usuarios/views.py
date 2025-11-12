# usuarios/views.py

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .models import Usuario
from .forms import UsuarioCreationForm, UsuarioChangeForm

# ============================================
# AUTENTICACIÓN
# ============================================

@never_cache
def login_view(request):
    """Vista de login con redirección según rol"""
    # Si el usuario ya está autenticado, redirigir según su rol
    if request.user.is_authenticated:
        if request.user.rol == 'admin':
            return redirect('administracion:dashboard')
        elif request.user.rol == 'cocinero':
            return redirect('cocina:dashboard')
        elif request.user.rol == 'cajero':
            return redirect('cajero:dashboard')
    
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        
        # Validaciones adicionales del lado del servidor
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        # Validar longitud de usuario
        if len(username) < 4:
            messages.error(request, 'El usuario debe tener al menos 4 caracteres.')
            return render(request, 'usuarios/login.html', {'form': form})
        
        if len(username) > 20:
            messages.error(request, 'El usuario no puede exceder 20 caracteres.')
            return render(request, 'usuarios/login.html', {'form': form})
        
        # Validar longitud de contraseña
        if len(password) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return render(request, 'usuarios/login.html', {'form': form})
        
        if len(password) > 20:
            messages.error(request, 'La contraseña no puede exceder 20 caracteres.')
            return render(request, 'usuarios/login.html', {'form': form})
        
        if form.is_valid():
            # Autenticación del usuario
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Verificar si las credenciales son correctas
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Verificar el rol del usuario y redirigir
                if user.rol == 'admin':
                    login(request, user)
                    return redirect('administracion:dashboard')
                elif user.rol == 'cocinero':
                    login(request, user)
                    return redirect('cocina:dashboard')
                elif user.rol == 'cajero':
                    login(request, user)
                    return redirect('cajero:dashboard')
                else:
                    messages.error(request, 'No tienes permisos para acceder.')
                    return redirect('usuarios:login')
            else:
                messages.error(request, 'Credenciales incorrectas. Verifica tu usuario y contraseña.')
        else:
            messages.error(request, 'Credenciales incorrectas. Verifica tu usuario y contraseña.')
    else:
        form = AuthenticationForm()

    return render(request, 'usuarios/login.html', {'form': form})


@never_cache
def logout_view(request):
    """Vista para cerrar sesión"""
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Has cerrado sesión correctamente.')
        
        # Crear respuesta de redirección
        response = redirect('usuarios:login')
        
        # Agregar headers para prevenir cache
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        
        return response
    
    # Si no es POST, redirigir al login
    return redirect('usuarios:login')


# ============================================
# PÁGINAS PÚBLICAS
# ============================================

def index(request):
    """Página principal"""
    return render(request, 'usuarios/index.html')


def sobre_nosotros(request):
    """Página sobre nosotros"""
    return render(request, 'usuarios/sobre_nosotros.html')


def servicios(request):
    """Página de servicios"""
    return render(request, 'usuarios/servicios.html')


def contactanos(request):
    """Página de contacto"""
    return render(request, 'usuarios/contactanos.html')


# ============================================
# CRUD DE USUARIOS (Accesible por admins)
# ============================================

@login_required
@never_cache
def lista_usuarios(request):
    """Lista todos los usuarios del sistema"""
    # Verificar que sea admin
    if request.user.rol != 'admin':
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('usuarios:login')
    
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})


@login_required
@never_cache
def crear_usuario(request):
    """Crea un nuevo usuario"""
    # Verificar que sea admin
    if request.user.rol != 'admin':
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('usuarios:login')
    
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, f'✅ Usuario "{user.username}" creado exitosamente!')
                return redirect('usuarios:lista_usuarios')
            except Exception as e:
                messages.error(request, f'❌ Error al crear el usuario: {str(e)}')
        else:
            messages.error(request, '❌ Por favor corrige los errores en el formulario.')
    else:
        form = UsuarioCreationForm()
    
    return render(request, 'usuarios/crear_usuario.html', {'form': form})


@login_required
@never_cache
def editar_usuario(request, id):
    """Edita un usuario existente"""
    # Verificar que sea admin
    if request.user.rol != 'admin':
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('usuarios:login')
    
    usuario = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        form = UsuarioChangeForm(request.POST, instance=usuario)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f'✅ Usuario "{usuario.username}" actualizado exitosamente!')
                return redirect('usuarios:lista_usuarios')
            except Exception as e:
                messages.error(request, f'❌ Error al actualizar el usuario: {str(e)}')
    else:
        form = UsuarioChangeForm(instance=usuario)
    
    return render(request, 'usuarios/editar_usuario.html', {'form': form, 'usuario': usuario})


@login_required
@never_cache
def eliminar_usuario(request, id):
    """Elimina un usuario"""
    # Verificar que sea admin
    if request.user.rol != 'admin':
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('usuarios:login')
    
    usuario = get_object_or_404(Usuario, id=id)
    
    # Prevenir que el admin se elimine a sí mismo
    if usuario.id == request.user.id:
        messages.error(request, '❌ No puedes eliminar tu propia cuenta.')
        return redirect('usuarios:lista_usuarios')
    
    if request.method == 'POST':
        username = usuario.username
        usuario.delete()
        messages.success(request, f'✅ Usuario "{username}" eliminado exitosamente!')
        return redirect('usuarios:lista_usuarios')
    
    return render(request, 'usuarios/eliminar_usuario.html', {'usuario': usuario})


# ============================================
# VISTAS DE PÁGINAS DE ERROR
# ============================================

def error_404(request, exception):
    """Vista personalizada para error 404 - Página no encontrada"""
    return render(request, '404.html', status=404)


def error_500(request):
    """Vista personalizada para error 500 - Error del servidor"""
    return render(request, '500.html', status=500)


def error_403(request, exception):
    """Vista personalizada para error 403 - Acceso denegado"""
    return render(request, '403.html', status=403)


# ============================================
# VISTAS DE PRUEBA (Solo para desarrollo)
# ⚠️ ELIMINAR ESTAS VISTAS EN PRODUCCIÓN
# ============================================

def test_404(request):
    """Vista para probar la página 404"""
    return render(request, '404.html', status=404)


def test_500(request):
    """Vista para probar la página 500"""
    return render(request, '500.html', status=500)


def test_403(request):
    """Vista para probar la página 403"""
    return render(request, '403.html', status=403)