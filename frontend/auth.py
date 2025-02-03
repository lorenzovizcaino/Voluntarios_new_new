"""
Módulo de autenticación que maneja el login de usuarios y la gestión de notificaciones.
Implementa la vista de inicio de sesión y determina el tipo de usuario para el enrutamiento.
"""

from pathlib import Path
import flet as ft
import json
import requests
import os
from time import sleep
from plyer import notification
from utils import API_URL_LOGIN, API_URL_DATOS_USER, set_id_usuario_logeado,path_fondo

def login(page: ft.Page):
    """
    Función principal que implementa la vista de login.
    
    Args:
        page (ft.Page): Objeto page de Flet
        
    Returns:
        ft.View: Vista de login configurada
    """
    # Configuración inicial de la ventana
    page.window_width = 400
    page.window_height = 400
    page.window_center()



    
    def check_and_show_notifications(user_id):
        """
        Verifica y muestra las notificaciones pendientes para un usuario.
        
        Args:
            user_id (int): ID del usuario que inicia sesión
            
        Efectos:
            - Lee el archivo de notificaciones del usuario
            - Muestra las notificaciones pendientes
            - Elimina el archivo de notificaciones después de mostrarlas
        """    
        
        try:
            notifications_file = Path(f"notifications/user_{user_id}_notifications.json")
            # Ruta al icono
            icon_path = Path("assets/images/icono.ico")            
            # Convertir la ruta del icono a string absoluto
            icon_absolute_path = str(icon_path.absolute())
            
            if notifications_file.exists():
                with open(notifications_file, 'r', encoding='utf-8') as f:
                    notifications = json.load(f)
                    
                # Mostrar cada notificación pendiente
                for notification_data in notifications:
                    try:
                        notification.notify(
                            title=notification_data["title"],
                            message=notification_data["message"],
                            app_icon=icon_absolute_path,
                            timeout=10,
                        )
                        
                        sleep(0.5) # Pausa entre notificaciones
                    except Exception as e:
                        print(f"Error al mostrar notificación: {e}")
                        
                # Limpiar las notificaciones mostradas
                os.remove(notifications_file)
                
        except Exception as e:
            print(f"Error al verificar notificaciones: {e}")
    

    
    def acceder(e):
        """
        Maneja el proceso de inicio de sesión.
        
        Args:
            e: Evento de Flet
            
        Efectos:
            - Valida credenciales contra el backend
            - Establece el ID de usuario en sesión
            - Redirecciona según el tipo de usuario
            - Muestra notificaciones pendientes
            - Actualiza mensajes de error si los hay
        """

        username = username_field.value
        password = password_field.value
        try:          

            params = {
                "username": username,
                "password": password
                }          
            
            # Verificar credenciales
            response = requests.get(API_URL_LOGIN, params=params)
            user_data = response.json()    
            if response.status_code ==200:
            
                id=user_data["id_user"]
                set_id_usuario_logeado(user_data["id_user"])

                # Obtener tipo de usuario
                url = f"{API_URL_DATOS_USER}/{id}"                
                response2=requests.get(url)                
                user_data2=response2.json()

                # Redireccionar según tipo de usuario
                if user_data2["tipo_usuario"] == "user":                     
                    page.go("/user")
                    #ver notificaciones pendientes
                    check_and_show_notifications(id)
                elif user_data2["tipo_usuario"] == "admin":  
                    page.go("/admin")                
                    
            else:
                error_text.value = "Usuario o contraseña incorrectos"
                page.update()
        except Exception as ex:
            error_text.value = f"Error de conexión: {ex}"
            page.update()

    # Componentes de la interfaz
    titulo = ft.Text("Login", size=24, weight=ft.FontWeight.BOLD)

    username_field = ft.TextField(label="Usuario")

    password_field = ft.TextField(label="Contraseña", 
                                  password=True, can_reveal_password=True)
    
    login_button = ft.ElevatedButton(
        "Iniciar sesión",          
        on_click=acceder,
        bgcolor=ft.colors.GREEN_400, 
        color=ft.colors.WHITE,        
        scale=1.4  
    )
    
    error_text = ft.Text("", color="red")

    # Organización de elementos en la interfaz
    row_titulo = ft.Row(controls=[titulo], 
                        alignment="center")

    row_login_button = ft.Row(controls=[login_button],
                              alignment="center")

    columna = ft.Column(controls=[row_titulo, 
                                  username_field, 
                                  password_field, 
                                  row_login_button, 
                                  error_text],
                        alignment="center",
                        spacing=30
                        )
    

    # Contenedor principal con imagen de fondo       
    main_container = ft.Container(
        content=ft.Stack(
            controls=[
                ft.Container(
                    expand=True,
                    bgcolor=ft.colors.TRANSPARENT,
                    image_src=path_fondo,    
                    image_fit=ft.ImageFit.COVER,
                    image_opacity=0.1,
                    #margin=ft.margin.only(top=50)  # La imagen comenzará 50px más abajo
                ),
                ft.Container(
                    content=columna,
                    expand=True,
                    bgcolor=ft.colors.TRANSPARENT,
                )
            ]
        ),
        expand=True
    )
    
    return ft.View("/login", controls=[main_container])
