from django.shortcuts import render

# Create your views here.
# administracion/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages

# ============================================
# DASHBOARD DE ADMINISTRADOR
# ============================================

@login_required
@never_cache
def admin_dashboard(request):
    """Dashboard principal del administrador"""
    # Verificar que el usuario es admin
    if request.user.rol != 'admin':
        messages.error(request, 'No tienes permisos para acceder a esta página.')
        return redirect('usuarios:login')
    
    # Limpiar mensajes anteriores que no deberían estar aquí
    storage = messages.get_messages(request)
    storage.used = True
    
    return render(request, 'administracion/admin_dashboard.html', {
        'usuario': request.user
    })