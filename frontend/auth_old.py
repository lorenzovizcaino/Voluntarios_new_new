import flet as ft
import json
import requests
from utils import API_URL_LOGIN, set_id_usuario_logeado,path_fondo

def login(page: ft.Page):
    page.window_width = 400
    page.window_height = 400
    page.window_center()

    
    def acceder(e):
        username = username_field.value
        password = password_field.value
        try:          

            params = {"username": username, "password": password}
            response = requests.get(API_URL_LOGIN, params=params)
            user_data = response.json()      

            if response.status_code == 200:
                set_id_usuario_logeado(user_data["id_user"]) 
                page.go("/user")
            elif response.status_code == 201:
                set_id_usuario_logeado(user_data["id_user"]) 
                page.go("/admin")
            else:
                error_text.value = "Usuario o contraseña incorrectos"
                page.update()
        except Exception as ex:
            error_text.value = f"Error de conexión: {ex}"
            page.update()

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
