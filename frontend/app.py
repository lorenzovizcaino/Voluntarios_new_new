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
# Añade el directorio raíz al path
sys.path.append(str(Path(__file__).parent.parent))
from api.database import *  
from api.routers.routers_users import routerlogin
from api.routers.routers_turnos import routerturnos
from api.routers.routers_tareas import routertareas
from api.routers.routers_tareas_asignadas import routertareas_asignadas
from api.routers.routers_datos_users import routerdatosuser

app = FastAPI()

app.include_router(routerlogin)
app.include_router(routerturnos)
app.include_router(routertareas)
app.include_router(routertareas_asignadas)
app.include_router(routerdatosuser)
init_db()



def main(page: ft.Page):
    page.title = "Voluntarios"
    page.theme_mode = ft.ThemeMode.LIGHT

    # Función para actualizar la vista según la ruta
    def cambiar_ruta(route):
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

    page.on_route_change = cambiar_ruta
    page.go("/login")

if __name__ == "__main__":
    
    # Inicia FastAPI en un thread separado
    import threading
    api_thread = threading.Thread(
        target=lambda: uvicorn.run(app, host="0.0.0.0", port=8000)
    )
    api_thread.daemon = True
    api_thread.start()
    
    # Inicia la aplicacion modo escritorio
    ft.app(target=main)
    # Inicia la aplicacion en un navegador
    #ft.app(target=main, view=ft.AppView.WEB_BROWSER)
    
