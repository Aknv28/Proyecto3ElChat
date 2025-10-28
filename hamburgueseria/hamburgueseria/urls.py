# hamburgueseria/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # URL para el panel de administración
    path('admin/', admin.site.urls),
    
    # Rutas de la app 'usuarios' (incluye index, login, dashboards, etc.)
    path('', include('usuarios.urls')),
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