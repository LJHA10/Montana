# gym_app/views.py
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .firebase import db  # Cambia esta línea para importar db desde firebase.py

def home_view(request):
    return render(request, 'gym_app/inventario.html')

def index(request):
    return render(request, 'gym_app/welcome.html')

def asistencia(request):
    asistencia_ref = db.collection('asistencia')
    asistencia_data = asistencia_ref.get()
    asistencia_list = [doc.to_dict() for doc in asistencia_data]
    return render(request, 'gym_app/asistencia.html', {'asistencia': asistencia_list})

def rutinas(request):
    return render(request, 'gym_app/rutinas.html')

def graficas(request):
    return render(request, 'gym_app/graficas.html')

def inventario(request):
    return render(request, 'gym_app/inventario.html')

# Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Autenticar al usuario administrador con Django
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Iniciar sesión en Django
            messages.success(request, f"Bienvenido {user.username}")
            return redirect('asistencia')  # Redirigir a la sección de asistencia
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
            return redirect('login')

    return render(request, 'gym_app/login.html')

# Registro de usuarios
def usuarios(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        weight = request.POST['weight']
        height = request.POST['height']
        diseases = request.POST['diseases']

        if password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden")
            return redirect('usuarios')

        usuario_data = {
            'username': username,
            'email': email,
            'password': password,
            'weight': float(weight),
            'height': float(height),
            'diseases': diseases,
        }

        db.collection('usuarios').add(usuario_data)
        messages.success(request, "Usuario registrado exitosamente")
        return redirect('usuarios')

    usuarios_ref = db.collection('usuarios').stream()
    usuarios = [usuario.to_dict() for usuario in usuarios_ref]

    return render(request, 'gym_app/usuarios.html', {'usuarios': usuarios})



# Inventario
def registrar_producto(request):
    if request.method == 'POST':
        nombre_producto = request.POST['nombre_producto']
        cantidad = request.POST['cantidad']
        categoria = request.POST['categoria']
        descripcion = request.POST['descripcion']

        if int(cantidad) <= 0:
            messages.error(request, "La cantidad debe ser mayor que cero")
            return redirect('registrar_producto')

        producto_data = {
            'nombre_producto': nombre_producto,
            'cantidad': int(cantidad),
            'categoria': categoria,
            'descripcion': descripcion,
        }

        try:
            db.collection('inventario').add(producto_data)
            messages.success(request, "Producto registrado exitosamente")
        except Exception as e:
            messages.error(request, f"Error al registrar el producto: {e}")

        return redirect('registrar_producto')

    inventario_ref = db.collection('inventario').stream()
    inventario = [producto.to_dict() for producto in inventario_ref]

    return render(request, 'gym_app/inventario.html', {'inventario': inventario})




# Asistencia
def registrar_asistencia(request):
    if request.method == 'POST':
        nombre_usuario = request.POST['nombre_usuario']
        fecha = request.POST['fecha']
        estado = request.POST['estado']  # Presente, Ausente, etc.

        asistencia_data = {
            'nombre_usuario': nombre_usuario,
            'fecha': fecha,
            'estado': estado,
        }

        try:
            db.collection('asistencia').add(asistencia_data)
            messages.success(request, "Asistencia registrada exitosamente")
        except Exception as e:
            messages.error(request, f"Error al registrar la asistencia: {e}")

        return redirect('asistencia')

    # Cargar datos de asistencia
    asistencia_ref = db.collection('asistencia').stream()
    asistencia = [asistencia.to_dict() for asistencia in asistencia_ref]

    return render(request, 'gym_app/asistencia.html', {'asistencia': asistencia})