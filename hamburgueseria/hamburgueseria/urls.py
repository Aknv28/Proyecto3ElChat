from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views

# Redirigir la raíz al login
def redirect_to_login(request):
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),  # Asegúrate de que este archivo 'usuarios/urls.py' tenga las rutas correctas para las vistas de usuarios

    # Aquí estamos configurando el logout para que redirija al login después de cerrar sesión
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Redirigir la raíz a la página de login
    path('', redirect_to_login),  # Redirige la raíz al login

    # Vista de login
    path('usuarios/login/', auth_views.LoginView.as_view(), name='login'),
]
