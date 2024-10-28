from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='welcome'),
    path('login/',views.login_view,name='login'),
    path('asistencia/', views.asistencia, name='asistencia'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('rutinas/', views.rutinas, name='rutinas'),
    path('graficas/', views.graficas, name='graficas'),
    path('inventario/', views.inventario, name='inventario'),
    path('registrar_producto/', views.registrar_producto, name='registrar_producto'),  # Agrega esta lín
]

    # path('registrar/', views.registrar_usuario, name='registrar_usuario'),