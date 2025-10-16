from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('cocinero_dashboard/', views.cocinero_dashboard, name='cocinero_dashboard'),
    path('cajero_dashboard/', views.cajero_dashboard, name='cajero_dashboard'),

]
