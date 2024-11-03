# gym_app/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from .firebase import db

def home_view(request):
    return render(request, 'gym_app/inventario.html')

def index(request):
    return render(request, 'gym_app/welcome.html')

@login_required
def asistencia(request):
    asistencia_ref = db.collection('asistencia')
    asistencia_data = asistencia_ref.get()
    asistencia_list = [doc.to_dict() for doc in asistencia_data]
    return render(request, 'gym_app/asistencia.html', {'asistencia': asistencia_list})

@login_required
def rutinas(request):
    return render(request, 'gym_app/rutinas.html')

@login_required
def graficas(request):
    return render(request, 'gym_app/graficas.html')

@login_required
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


# Logout
def logout_view(request):
    logout(request)  # Esto eliminará la sesión del usuario
    messages.success(request, "Has cerrado sesión exitosamente")
    return redirect('login')

# Registro de usuarios
@login_required
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



@login_required
def perfil_usuario(request):
    usuario = request.user  # Obtiene el superusuario

    if request.method == 'POST':
        # Actualiza los campos permitidos
        usuario.first_name = request.POST.get('first_name', usuario.first_name)
        usuario.last_name = request.POST.get('last_name', usuario.last_name)
        usuario.email = request.POST.get('email', usuario.email)
        
        # Si decides permitir cambiar la contraseña
        nueva_contrasena = request.POST.get('password')
        if nueva_contrasena:
            usuario.set_password(nueva_contrasena)  # Establece la nueva contraseña
            update_session_auth_hash(request, usuario)  # Mantiene al usuario autenticado
        usuario.save()  # Guarda los cambios

        messages.success(request, 'Tu perfil ha sido actualizado con éxito.')  # Mensaje de éxito

    return render(request, 'gym_app/perfil.html', {
        'usuario': usuario  # Pasa el objeto usuario al contexto
    })



# Inventario
@login_required
def registrar_producto(request):
    # Siempre mostrar la lista de productos en el inventario
    inventario_ref = db.collection('inventario').stream()
    inventario = [producto.to_dict() for producto in inventario_ref]

    if request.method == 'POST':
        nombre_producto = request.POST['nombre_producto']
        cantidad = request.POST['cantidad']
        categoria = request.POST['categoria']
        descripcion = request.POST['descripcion']

        # Validación de la cantidad
        if int(cantidad) <= 0:
            messages.error(request, "La cantidad debe ser mayor que cero")
            return render(request, 'gym_app/inventario.html', {'inventario': inventario})

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

        # Después de agregar el producto, vuelve a cargar la lista
        inventario_ref = db.collection('inventario').stream()
        inventario = [producto.to_dict() for producto in inventario_ref]

    # Renderiza la plantilla con la lista de productos
    return render(request, 'gym_app/inventario.html', {'inventario': inventario})



# Asistencia
@login_required
def registrar_asistencia(request):
    if request.method == 'POST':
        nombre_usuario = request.POST.get('nombre_usuario')
        fecha = request.POST.get('fecha')
        estado = request.POST.get('estado')  # Presente, Ausente, etc.

        if nombre_usuario and fecha and estado:
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
        else:
            messages.error(request, "Todos los campos son obligatorios")
    
    # Mostrar datos de asistencia
    asistencia_ref = db.collection('asistencia').stream()
    asistencia = [asistencia.to_dict() for asistencia in asistencia_ref]

    return render(request, 'gym_app/asistencia.html', {'asistencia': asistencia})

# Rutinas
@login_required
def registrar_rutina(request):
    if request.method == 'POST':
        nombre_rutina = request.POST.get('nombre_rutina')
        descripcion = request.POST.get('descripcion')
        duracion = request.POST.get('duracion')

        if nombre_rutina and descripcion and duracion:
            rutina_data = {
                'nombre_rutina': nombre_rutina,
                'descripcion': descripcion,
                'duracion': duracion,
            }

            try:
                db.collection('rutinas').add(rutina_data)
                messages.success(request, "Rutina registrada exitosamente")
            except Exception as e:
                messages.error(request, f"Error al registrar la rutina: {e}")

            return redirect('rutinas')
        else:
            messages.error(request, "Todos los campos son obligatorios")

    # Mostrar lista de rutinas
    rutinas_ref = db.collection('rutinas').stream()
    rutinas = [rutina.to_dict() for rutina in rutinas_ref]

    return render(request, 'gym_app/rutinas.html', {'rutinas': rutinas})