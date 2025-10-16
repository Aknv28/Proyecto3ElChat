from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


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
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

# Vista para el dashboard del Cocinero
def cocinero_dashboard(request):
    return render(request, 'cocinero_dashboard.html')

# Vista para el dashboard del Cajero
def cajero_dashboard(request):
    return render(request, 'cajero_dashboard.html')


