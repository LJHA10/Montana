from django.urls import path
from django.conf.urls.static import static
from gimnasio import settings
from . import views
from django.contrib import admin
from django.urls import path
from gym_app import views  # Asegúrate de importar las vistas necesarias
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='welcome'),
    path('login/',views.login_view,name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('asistencia/', views.registrar_asistencia, name='asistencia'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('ejercicios/', views.ejercicios, name='ejercicios'),
    path('ejercicio/editar/<str:ejercicio_id>/', views.editar_ejercicio, name='editar_ejercicio'),
    path('ejercicio/eliminar/<str:ejercicio_id>/', views.eliminar_ejercicio, name='eliminar_ejercicio'),
    path('rutinas/', views.crear_rutina, name='rutinas'),
    path('editar/<str:rutina_id>/', views.editar_rutina, name='editar_rutina'),
    path('rutinas/eliminar/<str:rutina_id>/', views.eliminar_rutina, name='eliminar_rutina'),
    path('graficas/', views.graficas, name='graficas'),
    path('inventario/', views.registrar_producto, name='inventario'),
    path('editar_producto/<str:producto_id>/', views.editar_producto, name='editar_producto'),
    path('eliminar_producto/<str:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('membresias/', views.membresias, name='membresias'),
    path('registrar_producto/', views.registrar_producto, name='registrar_producto'),
    path('registrar_asistencia/', views.registrar_asistencia, name='registrar_asistencia'),
    path('detalles_usuario/<str:usuario_id>/', views.detalles_usuario, name='detalles_usuario'),
    path('eliminar_usuario/<str:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('editar_usuario/<str:usuario_id>/', views.editar_usuario, name='editar_usuario'),
]