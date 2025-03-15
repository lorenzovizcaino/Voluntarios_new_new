"""
Módulo de utilidades que proporciona funciones comunes, gestión de estado
y configuración para toda la aplicación. Incluye manejo de URLs de API,
gestión de usuarios, notificaciones y utilidades generales.
"""

import os
import requests
import json
from pathlib import Path

# URLs de los endpoints de la API
API_URL_LOGIN = "http://127.0.0.1:8000/login"
API_URL_LOGIN_DATOS = "http://127.0.0.1:8000/logindatos"
API_URL_DATOS_USER = "http://127.0.0.1:8000/datosuser"
API_URL_TURNOS = "http://127.0.0.1:8000/turnos"
API_URL_TURNOS_DISPONIBLES = "http://127.0.0.1:8000/turnosdisponibles"
API_URL_TAREAS = "http://127.0.0.1:8000/tareas"
API_URL_TAREAS_EDIT = "http://127.0.0.1:8000/tareasedit"
API_URL_TAREAS_EDIT_COORDINADOR = "http://127.0.0.1:8000/tareaseditcoordinador"
API_URL_TAREAS_BORRAR = "http://127.0.0.1:8000/tareasborrarusuario"
API_URL_TAREAS_ASIGNADAS = "http://127.0.0.1:8000/tareasasignadas"
API_URL_USERS_ASIGNADOS = "http://127.0.0.1:8000/usersasignados"

# Ruta de la imagen de fondo
path_fondo = os.path.abspath(os.path.join("assets", "images", "3.png"))

# Variables globales para mantener estado
id_usuario_logeado = 0  # ID del usuario actualmente autenticado
selected_tab_index = 0  # Índice de la pestaña seleccionada en vista admin

def set_id_usuario_logeado(user_id):
    """
    Establece el ID del usuario que ha iniciado sesión.
    
    Args:
        user_id (int): ID del usuario autenticado
    """
    global id_usuario_logeado
    id_usuario_logeado = user_id

def get_id_usuario_logeado():
    """
    Obtiene el ID del usuario actualmente autenticado.
    
    Returns:
        int: ID del usuario logeado
    """
    return id_usuario_logeado



def obtener_nombre_usuario():
        """
        Obtiene el nombre del usuario actual desde la API.
        
        Returns:
            str: Nombre de usuario o None si hay error
        """
        try:
                
            response=requests.get(f"{API_URL_LOGIN}/{get_id_usuario_logeado()}")
            if response.status_code==200:                    
                data = response.json()
                nombre_usuario_logeado=data["username"]
                return nombre_usuario_logeado
                

                
            else:
                print(f"Error al obtener datos: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error en la conexión: {str(e)}")
            return None












def set_selected_tab_index(index):
    """
    Establece el índice de la pestaña seleccionada en la vista de admin.
    
    Args:
        index (int): Índice de la pestaña
    """
    global selected_tab_index
    selected_tab_index = index

def get_selected_tab_index():
    """
    Obtiene el índice de la pestaña actualmente seleccionada.
    
    Returns:
        int: Índice de la pestaña seleccionada
    """
    return selected_tab_index

def obtener_tarea_completa(id_tarea):
    """
    Obtiene la información completa de una tarea específica.
    
    Args:
        id_tarea (int): ID de la tarea a consultar
        
    Returns:
        dict: Información completa de la tarea o None si hay error
        
    Maneja los errores de conexión y respuesta de la API,
    registrando los problemas en la consola.
    """
    try:
        response = requests.get(f"{API_URL_TAREAS}/{id_tarea}")
        if response.status_code == 200:
            tarea_completa = response.json()
            return tarea_completa
        else:
            print(f"Error al obtener datos: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Error en la conexión: {str(e)}")
        return None

def guardar_notificacion(user_id, tarea_data, alta_baja_tarea):
    """
    Guarda una notificación pendiente para un usuario.
    
    Args:
        user_id (int): ID del usuario destinatario
        tarea_data (dict): Datos de la tarea asociada a la notificación
        alta_baja_tarea (bool): True si es asignación, False si es cancelación
        
    Efectos:
        - Crea el directorio de notificaciones si no existe
        - Guarda o actualiza el archivo JSON de notificaciones del usuario
        
    La función maneja la persistencia de notificaciones que serán
    mostradas al usuario cuando inicie sesión.
    """
    try:
        # Crear directorio de notificaciones si no existe
        notifications_dir = Path("notifications")
        notifications_dir.mkdir(exist_ok=True)
        
        notification_file = notifications_dir / f"user_{user_id}_notifications.json"
        
        # Preparar el mensaje según el tipo de notificación
        if alta_baja_tarea:
            notification_data = {
                "title": "Nueva tarea de voluntariado asignada:",
                "message": f"""Tarea: {tarea_data['tarea_name']}
                                Ubicación: {tarea_data['tarea_ubicacion']}
                                Fecha: {tarea_data['day']}/{tarea_data['month']}/{tarea_data['year']}
                                Turno: {tarea_data['turno']}"""
            }
        else:
            notification_data = {
                "title": "Se ha cancelado o modificado la tarea:",
                "message": f"""Tarea: {tarea_data['tarea_name']}
                                Ubicación: {tarea_data['tarea_ubicacion']}
                                Fecha: {tarea_data['day']}/{tarea_data['month']}/{tarea_data['year']}
                                Turno: {tarea_data['turno']}"""
            }
        
        # Cargar notificaciones existentes o crear nueva lista
        if notification_file.exists():
            with open(notification_file, 'r', encoding='utf-8') as f:
                notifications = json.load(f)
        else:
            notifications = []
            
        notifications.append(notification_data)
        
        # Guardar notificaciones actualizadas
        with open(notification_file, 'w', encoding='utf-8') as f:
            json.dump(notifications, f, ensure_ascii=False)
                
    except Exception as e:
        print(f"Error al guardar notificación: {e}")