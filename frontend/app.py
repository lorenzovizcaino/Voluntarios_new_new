import flet as ft
from auth import login
from user_view import user
from admin_view import admin, tarea_para_asignar

from admin_view_assign import admin_assign
from admin_view_edit import admin_edit

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
    ft.app(target=main)
