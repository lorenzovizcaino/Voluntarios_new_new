import flet as ft
from datetime import date, timedelta

def main(page: ft.Page):
    page.title = "Domingos de Diciembre 2024"
    
    def get_sundays():
        current = date(2024, 12, 1)
        while current.weekday() != 6:
            current += timedelta(days=1)
            
        sundays = []
        while current.month == 12:
            sundays.append(current.strftime("%d de Diciembre, 2024"))
            current += timedelta(days=7)
        return sundays

    sunday_list = ft.Column(
        controls=[
            ft.Text("Domingos de Diciembre 2024:", size=20, weight=ft.FontWeight.BOLD),
            *[ft.Text(sunday) for sunday in get_sundays()]
        ],
        spacing=10
    )
    
    # Añadir padding usando Container
    container = ft.Container(
        content=sunday_list,
        padding=20
    )
    
    page.add(container)

ft.app(target=main)