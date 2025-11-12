# hamburgueseria/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # URL para el panel de administración de Django
    path('admin/', admin.site.urls),
    
    # Apps del proyecto
    path('', include('usuarios.urls')),  # Páginas públicas, auth y gestión de usuarios
    path('administracion/', include('administracion.urls')),  # Dashboard y funciones de admin
    path('cajero/', include('cajero.urls')),  # Menú, pedidos y dashboard de cajero
    path('cocina/', include('cocina.urls')),  # Dashboard y gestión de pedidos en cocina
]

# ============================================
# CONFIGURACIÓN DE PÁGINAS DE ERROR
# ============================================
handler404 = 'usuarios.views.error_404'
handler500 = 'usuarios.views.error_500'
handler403 = 'usuarios.views.error_403'

# ============================================
# CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS
# Solo para desarrollo (DEBUG = True)
# ============================================
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    if hasattr(settings, 'MEDIA_URL') and hasattr(settings, 'MEDIA_ROOT'):
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)