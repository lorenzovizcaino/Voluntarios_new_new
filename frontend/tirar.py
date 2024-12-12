import flet as ft
from flet import Banner, ElevatedButton, Text, colors

def main(page: ft.Page):
    # Configuración inicial de la página
    page.title = "Ejemplo de Notificaciones"
    
    # Crear el banner para la notificación
    banner = Banner(
        bgcolor=colors.AMBER_100,
        leading=ft.Icon(ft.icons.NOTIFICATION_IMPORTANT, color=colors.AMBER, size=40),
        content=Text(
            "Esta es una notificación importante",
            color=colors.BLACK,
        ),
        actions=[
            ft.TextButton("Aceptar", on_click=lambda e: close_banner(e)),
            ft.TextButton("Cancelar", on_click=lambda e: close_banner(e)),
        ],
    )
    
    page.banner = banner
    
    def show_banner_click(e):
        page.banner.open = True
        page.update()
    
    def close_banner(e):
        page.banner.open = False
        page.update()
    
    # Crear el botón para mostrar la notificación
    btn = ElevatedButton("Mostrar Notificación", on_click=show_banner_click)
    
    # Agregar elementos a la página
    page.add(btn)

ft.app(target=main)