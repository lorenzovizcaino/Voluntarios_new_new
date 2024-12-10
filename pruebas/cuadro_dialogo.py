import flet as ft

def main(page: ft.Page):
    # Configuración inicial de la página
    page.title = "Ejemplo de Diálogo"
    page.window_width = 400
    page.window_height = 400

    def close_dialog(e):
        dialog.open = False
        page.update()

    def yes_clicked(e):
        result_text.value = "¡Has elegido SÍ!"
        close_dialog(e)
        page.update()

    def no_clicked(e):
        result_text.value = "Has elegido NO."
        close_dialog(e)
        page.update()

    def show_dialog(e):
        dialog.open = True
        page.update()

    # Crear el diálogo
    dialog = ft.AlertDialog(
        title=ft.Text("Pregunta importante"),
        content=ft.Text("¿Estás de acuerdo?"),
        actions=[
            ft.TextButton("Sí", on_click=yes_clicked),
            ft.TextButton("No", on_click=no_clicked),
        ],
    )

    # Texto para mostrar el resultado
    result_text = ft.Text("")

    # Botón para mostrar el diálogo
    page.add(
        ft.ElevatedButton("Mostrar diálogo", on_click=show_dialog),
        result_text
    )
    page.add(dialog)

ft.app(target=main)