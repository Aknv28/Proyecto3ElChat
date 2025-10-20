from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views

# Redirigir la raíz al index
def redirect_to_index(request):
    return redirect('index')

urlpatterns = [
    # URL para el panel de administración
    path('admin/', admin.site.urls),
    
    # Rutas de la app 'usuarios'
    path('usuarios/', include('usuarios.urls')),  # Asegúrate de que este archivo 'usuarios/urls.py' tenga las rutas correctas para las vistas de usuarios
    
    # Redirigir la raíz al index
    path('', redirect_to_index),  # Redirige la raíz al index
    
    # Vista de login
    path('usuarios/login/', auth_views.LoginView.as_view(), name='login'),
    
    # Logout, redirigiendo después de cerrar sesión
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
