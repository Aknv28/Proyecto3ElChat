# administracion/admin.py
from django.contrib import admin
from django.urls import path

class CustomAdminSite(admin.AdminSite):
    site_header = "Administración Hamburguesería"

    def get_urls(self):
        from .views import reportes_dashboard
        urls = super().get_urls()
        custom_urls = [
            path('reportes/', self.admin_view(reportes_dashboard), name='reportes_dashboard'),
        ]
        return custom_urls + urls

admin_site = CustomAdminSite(name='custom_admin')
