from api.database import session, init_db
from api.models.usuarios import User
from api.models.datos_usuarios import DatosUser

# Inicializar base de datos y agregar un usuario de prueba
init_db()
db = session()

admin = User(username="admin", password="admin")
antonio = User(username="antonio", password="123")
remi = User(username="remi", password="123")
antia = User(username="antia", password="123")
user4 = User(username="user4", password="123")
user5 = User(username="user5", password="123")



datosadmin=DatosUser(user_id=1,email="admin@gmail.com", direccion="C/Cuba 10", telefono="675506991",chat_id="",tipo_usuario="admin", config=False, coordinador=False, amigo="")

datosuser1=DatosUser(user_id=2,email="user1@gmail.com", direccion="C/Roma 10", telefono="675506990",chat_id="",tipo_usuario="user", config=False, coordinador=True, amigo="remi")

datosuser2=DatosUser(user_id=3,email="user2@gmail.com", direccion="C/Lisboa 10", telefono="615917522",chat_id="",tipo_usuario="user", config=False, coordinador=False, amigo="antonio")

datosuser3=DatosUser(user_id=4,email="user3@gmail.com", direccion="C/Paris 10", telefono="652946811",chat_id="",tipo_usuario="user", config=False, coordinador=False, amigo="user101")

datosuser4=DatosUser(user_id=5,email="user4@gmail.com", direccion="C/Londres 10", telefono="675506994",chat_id="",tipo_usuario="user", config=False, coordinador=True, amigo="")

datosuser5=DatosUser(user_id=6,email="user5@gmail.com", direccion="C/Berlin 10", telefono="675506995",chat_id="",tipo_usuario="user", config=False, coordinador=True, amigo="")

db.add(admin)
db.add(antonio)
db.add(remi)
db.add(antia)
db.add(user4)
db.add(user5)

db.add(datosadmin)
db.add(datosuser1)
db.add(datosuser2)
db.add(datosuser3)
db.add(datosuser4)
db.add(datosuser5)

db.commit()
db.close()


