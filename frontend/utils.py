import os
import requests



# URLs de API
API_URL_LOGIN = "http://127.0.0.1:8000/login"
API_URL_DATOS_USER = "http://127.0.0.1:8000/datosuser"
API_URL_TURNOS = "http://127.0.0.1:8000/turnos"
API_URL_TURNOS_DISPONIBLES = "http://127.0.0.1:8000/turnosdisponibles"
API_URL_TAREAS = "http://127.0.0.1:8000/tareas"
API_URL_TAREAS_EDIT = "http://127.0.0.1:8000/tareasedit"
API_URL_TAREAS_EDIT_COORDINADOR = "http://127.0.0.1:8000/tareaseditcoordinador"
API_URL_TAREAS_BORRAR = "http://127.0.0.1:8000/tareasborrarusuario"
API_URL_TAREAS_ASIGNADAS = "http://127.0.0.1:8000/tareasasignadas"

path_fondo = os.path.abspath(os.path.join("assets", "images", "3.png"))


# Estado global de usuario
id_usuario_logeado = 0

# indice del tab de la vista de admin
selected_tab_index = 0

def set_id_usuario_logeado(user_id):
    global id_usuario_logeado
    id_usuario_logeado = user_id

def get_id_usuario_logeado():
    return id_usuario_logeado


def set_selected_tab_index(index):
    global selected_tab_index
    selected_tab_index = index

def get_selected_tab_index():
    return selected_tab_index


def obtener_tarea_completa(id_tarea):
    try: 
        response=requests.get(f"{API_URL_TAREAS}/{id_tarea}")
        if response.status_code==200:
            tarea_completa=response.json()
            return tarea_completa
        else:
            print(f"Error al obtener datos: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error en la conexión: {str(e)}")
        return None