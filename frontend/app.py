"""
Módulo principal de la aplicación que integra la interfaz gráfica de Flet
con el backend de FastAPI. Maneja el enrutamiento entre vistas y la inicialización
de ambos servicios.
"""

import flet as ft
from auth import login
from user_view import user
from admin_view import admin, tarea_para_asignar
from admin_view_assign import admin_assign
from admin_view_edit import admin_edit

import uvicorn
from fastapi import FastAPI
import sys
from pathlib import Path

# Añadir directorio raíz al path para imports
sys.path.append(str(Path(__file__).parent.parent))

# Importaciones de la API
from api.database import *
from api.routers.routers_users import routerlogin
from api.routers.routers_turnos import routerturnos
from api.routers.routers_tareas import routertareas
from api.routers.routers_tareas_asignadas import routertareas_asignadas
from api.routers.routers_datos_users import routerdatosuser

# Inicialización de FastAPI
app = FastAPI()

# Registro de routers
app.include_router(routerlogin)
app.include_router(routerturnos)
app.include_router(routertareas)
app.include_router(routertareas_asignadas)
app.include_router(routerdatosuser)

# Inicialización de la base de datos
init_db()


def main(page: ft.Page):
    """
    Función principal que configura y maneja la interfaz gráfica de Flet.
    
    Args:
        page (ft.Page): Objeto page principal de Flet
        
    La función configura el tema, maneja el enrutamiento entre vistas
    y establece la vista inicial.
    """
    page.title = "RedAyuda"
    page.theme_mode = ft.ThemeMode.LIGHT

    def cambiar_ruta(route):
        """
        Actualiza la vista actual según la ruta especificada.
        
        Args:
            route: Ruta solicitada
            
        La función limpia las vistas existentes y carga la vista
        correspondiente a la ruta actual.
        """
        page.views.clear()
        if page.route == "/login":
            page.views.append(login(page))
        elif page.route == "/user":
            page.views.append(user(page))
        elif page.route == "/admin":
            page.views.append(admin(page))
        elif page.route == "/admin/assign":
            page.views.append(admin_assign(page))
        elif page.route == "/admin/edit":
            page.views.append(admin_edit(page))
        page.update()

    # Configurar manejo de rutas y establecer ruta inicial
    page.on_route_change = cambiar_ruta
    page.go("/login")


if __name__ == "__main__":
    # Iniciar FastAPI en un thread separado para que corra en paralelo
    # con la interfaz gráfica
    import threading
    api_thread = threading.Thread(
        target=lambda: uvicorn.run(app, host="0.0.0.0", port=8000)
    )
    api_thread.daemon = True  # El thread se cerrará cuando el programa principal termine
    api_thread.start()
    
    # Iniciar la aplicación Flet
    ft.app(target=main)  # Modo escritorio
    # ft.app(target=main, view=ft.AppView.WEB_BROWSER)  # Modo navegador 