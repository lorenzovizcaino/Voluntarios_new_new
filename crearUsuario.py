from api.database import session, init_db
from api.models.usuarios import User
from api.models.datos_usuarios import DatosUser

# Inicializar base de datos y agregar un usuario de prueba
init_db()
db = session()

admin = User(username="admin", password="admin")
user1 = User(username="user1", password="123")
user2 = User(username="user2", password="123")
user3 = User(username="user3", password="123")
user4 = User(username="user4", password="123")
user5 = User(username="user5", password="123")



datosadmin=DatosUser(user_id=1,email="admin@gmail.com", direccion="C/Cuba 10", telefono="675506990",tipo_usuario="admin", config=False, coordinador=False, amigo="")

datosuser1=DatosUser(user_id=2,email="user1@gmail.com", direccion="C/Roma 10", telefono="675506991",tipo_usuario="user", config=False, coordinador=True, amigo="user2")

datosuser2=DatosUser(user_id=3,email="user2@gmail.com", direccion="C/Lisboa 10", telefono="675506992",tipo_usuario="user", config=False, coordinador=False, amigo="user1")

datosuser3=DatosUser(user_id=4,email="user3@gmail.com", direccion="C/Paris 10", telefono="675506993",tipo_usuario="user", config=False, coordinador=False, amigo="user101")

datosuser4=DatosUser(user_id=5,email="user4@gmail.com", direccion="C/Londres 10", telefono="675506994",tipo_usuario="user", config=False, coordinador=True, amigo="")

datosuser5=DatosUser(user_id=6,email="user5@gmail.com", direccion="C/Berlin 10", telefono="675506995",tipo_usuario="user", config=False, coordinador=True, amigo="")

db.add(admin)
db.add(user1)
db.add(user2)
db.add(user3)
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


