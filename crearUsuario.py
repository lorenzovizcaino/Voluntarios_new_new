"""
Script de inicialización de la base de datos.
Crea usuarios de prueba y sus datos asociados para el sistema de voluntariado.
"""

from api.database import session, init_db
from api.models.usuarios import User
from api.models.datos_usuarios import DatosUser

# Inicializar base de datos
init_db()
db = session()

# Creación de usuarios base con credenciales
admin = User(username="admin", password="admin")
antonio = User(username="antonio", password="123")
remi = User(username="remi", password="123")
antia = User(username="antia", password="123")
user4 = User(username="user4", password="123")
user5 = User(username="user5", password="123")

# Creación de datos extendidos para cada usuario
# Admin: Usuario administrador del sistema
datosadmin = DatosUser(
    user_id=1,
    email="admin@gmail.com",
    direccion="C/Cuba 10",
    telefono="675506991",
    chat_id="",
    tipo_usuario="admin",
    config=False,
    coordinador=False,
    amigo=""
)

# Usuario 1: Coordinador con amigo asignado
datosuser1 = DatosUser(
    user_id=2,
    email="user1@gmail.com",
    direccion="C/Roma 10",
    telefono="675506990",
    chat_id="",
    tipo_usuario="user",
    config=False,
    coordinador=True,
    amigo="remi"
)

# Usuario 2: Voluntario regular con amigo asignado
datosuser2 = DatosUser(
    user_id=3,
    email="user2@gmail.com",
    direccion="C/Lisboa 10",
    telefono="615917522",
    chat_id="",
    tipo_usuario="user",
    config=False,
    coordinador=False,
    amigo="antonio"
)

# Usuario 3: Voluntario regular sin amigo
datosuser3 = DatosUser(
    user_id=4,
    email="user3@gmail.com",
    direccion="C/Paris 10",
    telefono="652946811",
    chat_id="",
    tipo_usuario="user",
    config=False,
    coordinador=False,
    amigo=""
)

# Usuario 4: Coordinador sin amigo asignado
datosuser4 = DatosUser(
    user_id=5,
    email="user4@gmail.com",
    direccion="C/Londres 10",
    telefono="675506994",
    chat_id="",
    tipo_usuario="user",
    config=False,
    coordinador=True,
    amigo=""
)

# Usuario 5: Coordinador sin amigo asignado
datosuser5 = DatosUser(
    user_id=6,
    email="user5@gmail.com",
    direccion="C/Berlin 10",
    telefono="675506995",
    chat_id="",
    tipo_usuario="user",
    config=False,
    coordinador=True,
    amigo=""
)

# Agregar usuarios base a la sesión
db.add(admin)
db.add(antonio)
db.add(remi)
db.add(antia)
db.add(user4)
db.add(user5)

# Agregar datos extendidos a la sesión
db.add(datosadmin)
db.add(datosuser1)
db.add(datosuser2)
db.add(datosuser3)
db.add(datosuser4)
db.add(datosuser5)

# Confirmar cambios y cerrar sesión
db.commit()
db.close()