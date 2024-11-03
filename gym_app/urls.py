from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='welcome'),
    path('login/',views.login_view,name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('asistencia/', views.registrar_asistencia, name='asistencia'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('rutinas/', views.registrar_rutina, name='rutinas'),
    path('graficas/', views.graficas, name='graficas'),
    path('inventario/', views.registrar_producto, name='inventario'),
    path('registrar_producto/', views.registrar_producto, name='registrar_producto'),  # Agrega esta lín
]

    # path('registrar/', views.registrar_usuario, name='registrar_usuario'),