from django.shortcuts import render, redirect
from django.contrib import messages
from firebase_admin import credentials, firestore, storage
import uuid
# gym_app/views.py
from google.cloud import firestore
from datetime import datetime
from datetime import datetime
import calendar
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from firebase_admin import firestore
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from datetime import datetime
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
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

@login_required
def home_view(request):
    return render(request, 'gym_app/inventario.html')
@login_required
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
@login_required
def membresias(request):
    return render(request, 'gym_app/membresias.html')



# LOGIN 
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

# perfil del administrador
@login_required
def perfil_usuario(request):
    usuario = request.user  # Obtiene el usuario autenticado

    if request.method == 'POST':
        # Obtén los valores del formulario
        first_name = request.POST.get('first_name', usuario.first_name)
        last_name = request.POST.get('last_name', usuario.last_name)
        email = request.POST.get('email', usuario.email)
        nueva_contrasena = request.POST.get('new_password')
        confirmar_contrasena = request.POST.get('confirm_password')
        
        # Actualiza la información básica del usuario
        usuario.first_name = first_name
        usuario.last_name = last_name
        usuario.email = email
        
        # Validación y actualización de la contraseña
        if nueva_contrasena or confirmar_contrasena:
            if nueva_contrasena == confirmar_contrasena:
                if len(nueva_contrasena) >= 8:  # Validación de longitud mínima
                    usuario.set_password(nueva_contrasena)
                    update_session_auth_hash(request, usuario)  # Mantiene al usuario autenticado
                    messages.success(request, 'Contraseña actualizada con éxito.')
                else:
                    messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
                    return render(request, 'gym_app/perfil.html', {'usuario': usuario})
            else:
                messages.error(request, 'Las contraseñas no coinciden.')
                return render(request, 'gym_app/perfil.html', {'usuario': usuario})

        usuario.save()  # Guarda los cambios
        messages.success(request, 'Tu perfil ha sido actualizado con éxito.')

        return redirect('perfil_usuario')  # Redirige al perfil para mostrar los cambios

    return render(request, 'gym_app/perfil.html', {
        'usuario': usuario  # Pasa el objeto usuario al contexto
    })


@login_required
def registrar_producto(request):
    inventario_ref = db.collection('inventario').stream()
    inventario = [{'id': producto.id, **producto.to_dict()} for producto in inventario_ref]

    if request.method == 'POST':
        nombre_producto = request.POST['nombre_producto']
        cantidad = request.POST['cantidad']
        categoria = request.POST['categoria']
        descripcion = request.POST['descripcion']

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

        inventario_ref = db.collection('inventario').stream()
        inventario = [{'id': producto.id, **producto.to_dict()} for producto in inventario_ref]

    return render(request, 'gym_app/inventario.html', {'inventario': inventario})


@login_required
def editar_producto(request, producto_id):
    producto_ref = db.collection('inventario').document(producto_id)
    producto_doc = producto_ref.get()

    if not producto_doc.exists:
        messages.error(request, "El producto no existe.")
        return redirect('registrar_producto')

    producto = {'id': producto_id, **producto_doc.to_dict()}

    if request.method == 'POST':
        nombre_producto = request.POST['nombre_producto']
        cantidad = request.POST['cantidad']
        categoria = request.POST['categoria']
        descripcion = request.POST['descripcion']

        if not nombre_producto or not cantidad or not categoria or not descripcion:
            messages.error(request, "Por favor, completa todos los campos.")
            return render(request, 'gym_app/editar_producto.html', {'producto': producto})

        try:
            producto_ref.update({
                'nombre_producto': nombre_producto,
                'cantidad': int(cantidad),
                'categoria': categoria,
                'descripcion': descripcion,
            })
            messages.success(request, "Producto actualizado exitosamente.")
            return redirect('registrar_producto')
        except Exception as e:
            messages.error(request, f"Error al actualizar el producto: {e}")

    return render(request, 'gym_app/editar_producto.html', {'producto': producto})


@login_required
def eliminar_producto(request, producto_id):
    producto_ref = db.collection('inventario').document(producto_id)

    try:
        producto_ref.delete()
        messages.success(request, "Producto eliminado exitosamente.")
    except Exception as e:
        messages.error(request, f"Error al eliminar el producto: {e}")

    return redirect('registrar_producto')


# Asistencia //Registro de asistencia
@login_required
def registrar_asistencia(request):
    search_query = request.GET.get('search_query', '').strip()
    usuarios = []

    # Obtener todos los usuarios de la colección 'users'
    users_ref = db.collection('users').stream()

    if search_query:
        # Filtrar usuarios por coincidencia de nombre
        for user in users_ref:
            user_data = user.to_dict()
            user_data['id'] = user.id  # Añadir el id del usuario de Firestore
            if search_query.lower() in user_data.get('name', '').lower():
                usuarios.append(user_data)
    else:
        # Mostrar todos los usuarios si no hay búsqueda
        for user in users_ref:
            user_data = user.to_dict()
            user_data['id'] = user.id  # Añadir el id del usuario de Firestore
            usuarios.append(user_data)

    if request.method == 'POST':
        # Obtener los datos del formulario
        usuario_id = request.POST.get('usuario_id')  # Obtener el ID del usuario
        nombre_usuario = request.POST.get('nombre_usuario')
        fecha = datetime.now().strftime('%Y-%m-%d')

        if nombre_usuario and usuario_id:
            # Crear el objeto de datos de la asistencia
            asistencia_data = {
                'usuario_id': usuario_id,  # ID del usuario
                'timestamp': firestore.SERVER_TIMESTAMP,
                'name': nombre_usuario,
                # Añadir el ID del usuario para asociarlo
            }

            try:
                # Registrar la asistencia en la colección 'attendance'
                db.collection('attendance').add(asistencia_data)
                messages.success(request, f"Asistencia registrada exitosamente para {nombre_usuario}")
            except Exception as e:
                messages.error(request, f"Error al registrar la asistencia: {e}")

            return redirect('asistencia')  # Redirigir a la vista de asistencia
        else:
            messages.error(request, "Falta información para registrar la asistencia")

    return render(request, 'gym_app/asistencia.html', {'usuarios': usuarios})
   

# Detalles   //Consulta de la informacion del usuario atravez de su id
@login_required
def detalles_usuario(request, usuario_id):
    usuario_ref = db.collection('users').document(usuario_id)
    usuario = usuario_ref.get()

    if usuario.exists:
        # Obtener los datos del usuario como un diccionario
        usuario_data = usuario.to_dict()

        # Obtener las fechas de asistencia del usuario
        asistencia_ref = db.collection('attendance').where('usuario_id', '==', usuario_id).stream()

        # Lista de fechas de asistencia formateadas a 'YYYY-MM-DD'
        fechas_asistencia = [
            asistencia.to_dict().get('timestamp').strftime('%Y-%m-%d')
            for asistencia in asistencia_ref
            if asistencia.to_dict().get('timestamp') is not None
        ]

        # Obtener el mes y año actual
        now = datetime.now()
        current_month = now.strftime('%Y-%m')  # formato YYYY-MM
        month = now.month
        year = now.year
        
        # Generar el calendario del mes
        month_days = calendar.monthcalendar(year, month)

        # Enviar los datos a la plantilla
        return render(request, 'gym_app/detalles_usuario.html', {
            'usuario': usuario_data,
            'fechas_asistencia': fechas_asistencia,
            'current_month': current_month,
            'month_days': month_days,
            'usuario_id': usuario_id, 
        })
    else:
        # Si no se encuentra el usuario
        return HttpResponse("Usuario no encontrado", status=404)


#eliminar usuarios
@login_required
def eliminar_usuario(request, usuario_id):
    usuario_ref = db.collection('users').document(usuario_id)
    usuario = usuario_ref.get()

    if usuario.exists:
        usuario_ref.delete()
        return redirect('asistencia')  # Cambia 'nombre_de_la_ruta_donde_redirigir_despues' por tu ruta deseada
    else:
        return HttpResponse("Usuario no encontrado", status=404)


#Editar user
def editar_usuario(request, usuario_id):
    usuario_ref = db.collection('users').document(usuario_id)
    usuario = usuario_ref.get()

    if usuario.exists:
        if request.method == 'POST':
            # Actualizar los datos con lo enviado en el formulario
            try:
                height = float(request.POST.get('height'))
                weight = float(request.POST.get('weight'))
            except ValueError:
                # Manejar el caso donde no se pueda convertir a float
                return HttpResponse("Datos inválidos para altura o peso", status=400)

            usuario_ref.update({
                'name': request.POST.get('name'),
                'height': height,
                'weight': weight,
                'diseases': request.POST.get('diseases'),
            })
            return redirect('detalles_usuario', usuario_id=usuario_id)

        # Si la solicitud es GET, renderiza el template con los datos del usuario
        usuario_data = usuario.to_dict()
        return render(request, 'gym_app/editar_usuario.html', {
            'usuario': usuario_data,
            'usuario_id': usuario_id,
        })
    else:
        return HttpResponse("Usuario no encontrado", status=404)


#Resgitar ejercicios
# Registrar ejercicios
@login_required
def ejercicios(request):
    if request.method == 'POST':
        nombre_ejercicio = request.POST.get('nombre_ejercicio')
        descripcion = request.POST.get('descripcion')
        consejos = request.POST.get('consejos')

        if nombre_ejercicio and descripcion:
            # Guardar los datos en Firestore
            ejercicio_data = {
                'nombre_ejercicio': nombre_ejercicio,
                'descripcion': descripcion,
                'consejos': consejos
            }
            db.collection('ejercicios').add(ejercicio_data)

            messages.success(request, "Ejercicio registrado exitosamente")
            return redirect('ejercicios')
        else:
            messages.error(request, "Todos los campos obligatorios deben estar completos")

    # Filtrado por búsqueda
    search_query = request.GET.get('search', '')
    if search_query:
        # Recupera todos los ejercicios de Firestore
        ejercicios_snapshot = db.collection('ejercicios').get()
        ejercicios = [{
            'id': ej.id,  # Agregar el 'id' de Firestore como un campo adicional
            **ej.to_dict()
        } for ej in ejercicios_snapshot]

        # Filtrar los ejercicios por coincidencia parcial con el nombre
        ejercicios = [ejercicio for ejercicio in ejercicios if search_query.lower() in ejercicio['nombre_ejercicio'].lower()]
    else:
        # Si no hay búsqueda, mostrar todos los ejercicios
        ejercicios_snapshot = db.collection('ejercicios').get()
        ejercicios = [{
            'id': ej.id,
            **ej.to_dict()
        } for ej in ejercicios_snapshot]

    return render(request, 'gym_app/registrar_ejercicio.html', {'ejercicios': ejercicios})



#Seccion del ejercicio
#editar el ejercicio
@login_required
def editar_ejercicio(request, ejercicio_id):
    # Obtener el ejercicio desde Firestore por su ID
    ejercicio_ref = db.collection('ejercicios').document(ejercicio_id)
    ejercicio = ejercicio_ref.get()

    if ejercicio.exists:
        # Convertimos el documento a un diccionario de Python
        ejercicio_data = ejercicio.to_dict()
        ejercicio_data['id'] = ejercicio.id  # Añadir el ID a los datos
    else:
        # Si el ejercicio no existe, redirigir o mostrar un error
        messages.error(request, "Ejercicio no encontrado.")
        return redirect('ejercicios')  # Redirigir a la lista de ejercicios o donde desees

    # Si el formulario se envía (actualización del ejercicio)
    if request.method == 'POST':
        nombre_ejercicio = request.POST.get('nombre_ejercicio')
        descripcion = request.POST.get('descripcion')
        consejos = request.POST.get('consejos')

        # Actualizar los datos del ejercicio en Firestore
        if nombre_ejercicio and descripcion:
            ejercicio_ref.update({
                'nombre_ejercicio': nombre_ejercicio,
                'descripcion': descripcion,
                'consejos': consejos
            })
            messages.success(request, "Ejercicio actualizado exitosamente.")
            return redirect('ejercicios')  # Redirigir a la lista de ejercicios

        else:
            messages.error(request, "Todos los campos obligatorios deben estar completos")

    # Si el método es GET, se muestra el formulario de edición con los datos actuales
    return render(request, 'gym_app/editar_ejercicio.html', {'ejercicio': ejercicio_data})

#Crear rutina
@login_required
def crear_rutina(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        rutina_nombre = request.POST.get('rutina_nombre')
        ejercicios_seleccionados = request.POST.getlist('ejercicios')
        repeticiones = request.POST.get('repeticiones')
        series = request.POST.get('series')

        # Validar que todos los campos requeridos estén presentes
        if not rutina_nombre or not ejercicios_seleccionados or not repeticiones or not series:
            messages.error(request, 'Todos los campos son obligatorios.')
            return redirect('crear_rutina')

        try:
            # Crear la rutina en la base de datos
            nueva_rutina = db.collection('rutinas').document()
            nueva_rutina.set({
                'nombre': rutina_nombre,
            })

            # Añadir los ejercicios a la subcolección de ejercicios
            for ejercicio in ejercicios_seleccionados:
                nueva_rutina.collection('ejercicios').add({
                    'nombre_ejercicio': ejercicio,
                    'repeticiones': int(repeticiones),
                    'series': int(series),
                })

            messages.success(request, 'Rutina creada exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al crear la rutina: {e}')

        return redirect('rutinas')

    # Código para mostrar rutinas y ejercicios (como en tu ejemplo original)
    search_query = request.GET.get('search', '').strip()
    rutinas = db.collection('rutinas')

    if search_query:
        rutinas = rutinas.where('nombre', '>=', search_query).where('nombre', '<=', search_query + '\uf8ff')

    rutinas = rutinas.stream()
    rutinas_lista = []
    for rutina in rutinas:
        rutina_data = rutina.to_dict()
        rutina_data['id'] = rutina.id
        ejercicios_snapshot = rutina.reference.collection('ejercicios').stream()
        ejercicios_rutina = [ejercicio.to_dict() for ejercicio in ejercicios_snapshot]
        rutina_data['ejercicios'] = ejercicios_rutina
        rutinas_lista.append(rutina_data)

    ejercicios = db.collection('ejercicios').stream()
    ejercicios_lista = [ejercicio.to_dict() for ejercicio in ejercicios]

    return render(request, 'gym_app/crear_rutina.html', {
        'rutinas': rutinas_lista,
        'ejercicios': ejercicios_lista,
    })




# Editar rutina
@login_required
def editar_rutina(request, rutina_id):
    try:
        # Obtener la referencia de la rutina usando el ID
        rutina_ref = db.collection('rutinas').document(rutina_id)
        rutina_data = rutina_ref.get().to_dict()

        # Verificar si la rutina existe
        if not rutina_data:
            messages.error(request, 'La rutina no existe.')
            return redirect('rutinas')

        # Obtener los ejercicios de la rutina
        ejercicios_snapshot = rutina_ref.collection('ejercicios').stream()
        ejercicios_rutina = [{'id': ejercicio.id, **ejercicio.to_dict()} for ejercicio in ejercicios_snapshot]
        nombres_ejercicios_rutina = [ej['nombre_ejercicio'] for ej in ejercicios_rutina]  # Solo nombres

        # Obtener la lista de todos los ejercicios disponibles
        ejercicios_disponibles = db.collection('ejercicios').stream()
        ejercicios_lista = [ejercicio.to_dict() for ejercicio in ejercicios_disponibles]

        if request.method == 'POST':
            # Actualizar el nombre de la rutina y los ejercicios seleccionados
            rutina_nombre = request.POST.get('rutina_nombre')
            ejercicios_seleccionados = request.POST.getlist('ejercicios')
            repeticiones = request.POST.get('repeticiones')
            series = request.POST.get('series')

            if not rutina_nombre or not ejercicios_seleccionados or not repeticiones or not series:
                messages.error(request, 'Todos los campos son obligatorios.')
                return redirect('editar_rutina', rutina_id=rutina_id)

            # Actualizar nombre de la rutina en Firestore
            rutina_ref.update({'nombre': rutina_nombre})

            # Eliminar ejercicios existentes en la rutina
            for ejercicio in ejercicios_rutina:
                rutina_ref.collection('ejercicios').document(ejercicio['id']).delete()

            # Añadir los nuevos ejercicios seleccionados
            for ejercicio in ejercicios_seleccionados:
                rutina_ref.collection('ejercicios').add({
                    'nombre_ejercicio': ejercicio,
                    'repeticiones': int(repeticiones),
                    'series': int(series),
                })

            messages.success(request, 'Rutina actualizada exitosamente.')
            return redirect('rutinas')

        # Pasar los datos al template
        return render(request, 'gym_app/editar_rutina.html', {
            'rutina': rutina_data,  # Incluir los datos de la rutina
            'rutina_id': rutina_ref.id,  # Pasar el id de la rutina
            'ejercicios_rutina': ejercicios_rutina,
            'ejercicios_disponibles': ejercicios_lista,
            'nombres_ejercicios_rutina': nombres_ejercicios_rutina,  # Lista de nombres de ejercicios
        })
    
    except Exception as e:
        messages.error(request, f'Error al cargar la rutina: {e}')
        return redirect('rutinas')






@login_required
def eliminar_rutina(request, rutina_id):
    try:
        # Obtener la referencia de la rutina
        rutina_ref = db.collection('rutinas').document(rutina_id)

        # Eliminar todos los ejercicios de la rutina
        ejercicios_snapshot = rutina_ref.collection('ejercicios').stream()
        for ejercicio in ejercicios_snapshot:
            ejercicio.reference.delete()

        # Eliminar la rutina
        rutina_ref.delete()

        messages.success(request, 'Rutina eliminada exitosamente.')
    except Exception as e:
        messages.error(request, f'Error al eliminar la rutina: {e}')

    return redirect('rutinas')



#Eliminar el ejercicio
@login_required
def eliminar_ejercicio(request, ejercicio_id):
    if request.method == 'POST':
        # Recuperamos el ejercicio de Firestore
        ejercicio_ref = db.collection('ejercicios').document(ejercicio_id)
        ejercicio = ejercicio_ref.get()

        if ejercicio.exists:
            # Eliminamos el ejercicio de Firestore
            ejercicio_ref.delete()
            messages.success(request, "Ejercicio eliminado exitosamente.")
        else:
            messages.error(request, "El ejercicio no existe.")

        # Redirigimos de vuelta a la lista de ejercicios
        return redirect('ejercicios')

    # Si no es un POST, redirigimos a la página de ejercicios
    return redirect('ejercicios')

#Graficas
@login_required
def graficas(request):
    # Obtener rutinas desde Firebase
    rutinas = db.collection('rutinas').stream()

    # Inicializar listas para almacenar las fechas y cantidades
    fechas = []
    cantidades = []

    for rutina in rutinas:
        # Suponiendo que cada rutina tiene una fecha
        rutina_data = rutina.to_dict()
        fecha = rutina_data.get('fecha', 'Desconocida')  # Cambia 'fecha' por el campo real
        fechas.append(fecha)

    # Contar las rutinas por fecha (en este caso, las fechas serán las etiquetas del gráfico)
    # Esto es solo un ejemplo, puedes procesar los datos como desees
    from collections import Counter
    contador = Counter(fechas)
    
    # Extraemos las fechas y las cantidades para pasarlas al gráfico
    fechas = list(contador.keys())
    cantidades = list(contador.values())

    return render(request, 'gym_app/graficas.html', {
        'fechas': fechas,
        'cantidades': cantidades,
    })


# Registro de usuarios //Quedara pendiente
@login_required
def usuarios(request):
    if request.method == 'POST':
        name = request.POST['username']  # Usamos 'username' como 'name'
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        weight = request.POST['weight']
        height = request.POST['height']
        diseases = request.POST['diseases']

        if password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden")
            return redirect('usuarios')

        # Crear el objeto con los nombres de campo alineados con la app móvil
        usuario_data = {
            'name': name,          # Guardar como 'name'
            'email': email,
            'password': password,  # Puedes considerar encriptar la contraseña antes de guardar
            'weight': float(weight),  # Guardar como 'weight'
            'diseases': diseases,   # Guardar como 'diseases'
            'timestamp': firestore.SERVER_TIMESTAMP  # Simular el 'FieldValue.serverTimestamp()'
        }

        # Guardar en la colección 'users'
        db.collection('users').add(usuario_data)
        messages.success(request, "Usuario registrado exitosamente")
        return redirect('usuarios')

    # Obtener los usuarios ya registrados
    usuarios_ref = db.collection('users').stream()
    usuarios = [usuario.to_dict() for usuario in usuarios_ref]

    return render(request, 'gym_app/usuarios.html', {'usuarios': usuarios})
