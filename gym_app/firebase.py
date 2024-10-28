import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


# Cargar la clave de cuenta de servicio
cred = credentials.Certificate('firebase_credentials.json')

# Inicializar la aplicación Firebase
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Obtener la base de datos Firestore
db = firestore.client()