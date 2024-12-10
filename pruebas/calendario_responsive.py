import flet as ft
from datetime import datetime
import calendar

class VolunteerCalendar(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.current_date = datetime.now()
        
    def build(self):
        # Función para determinar si estamos en móvil
        def is_mobile(e):
            return self.page.window_width < 768 if self.page else True
            
        # Función para construir el día en vista móvil
        def build_mobile_day(day):
            return ft.Container(
                content=ft.Column([
                    ft.Text(f"{day}", size=20, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        ft.Column([
                            ft.Checkbox(label="T1", scale=1.2),
                            ft.Checkbox(label="T2", scale=1.2),
                        ]),
                        ft.Column([
                            ft.Checkbox(label="T3", scale=1.2),
                            ft.Checkbox(label="T4", scale=1.2),
                        ]),
                    ], alignment=ft.MainAxisAlignment.SPACE_AROUND)
                ]),
                padding=10,
                bgcolor=ft.colors.LIGHT_GREEN_50,
                border_radius=10,
                border=ft.border.all(1, ft.colors.GREY_400),
                margin=5
            )

        # Función para construir el día en vista desktop
        def build_desktop_day(day):
            return ft.Container(
                content=ft.Column([
                    ft.Text(f"{day}"),
                    ft.Column([
                        ft.Checkbox(label="T1", scale=0.8),
                        ft.Checkbox(label="T2", scale=0.8),
                        ft.Checkbox(label="T3", scale=0.8),
                        ft.Checkbox(label="T4", scale=0.8),
                    ], spacing=0)
                ], spacing=2),
                padding=5,
                bgcolor=ft.colors.LIGHT_GREEN_50,
                border_radius=10,
                border=ft.border.all(1, ft.colors.GREY_400),
                margin=2
            )

        # Tabs de navegación
        tabs = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(
                    text="Calendario de disponibilidad",
                    icon=ft.icons.CALENDAR_MONTH
                ),
                ft.Tab(
                    text="Ver Tareas asignadas",
                    icon=ft.icons.LIST_ALT
                ),
            ],
        )

        # Título del mes
        month_title = ft.Text(
            "December 2024",
            size=24,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )

        # Construir el calendario
        cal = calendar.monthcalendar(2024, 12)
        days_of_week = ['L', 'M', 'X', 'J', 'V', 'S', 'D']

        def build_calendar(e=None):
            is_mob = is_mobile(e)
            if is_mob:
                # Vista móvil
                return ft.Column(
                    [build_mobile_day(day) for week in cal for day in week if day != 0],
                    scroll=ft.ScrollMode.AUTO,
                    height=500,
                )
            else:
                # Vista desktop
                weeks = []
                # Agregar días de la semana
                header = ft.Row(
                    [ft.Container(
                        ft.Text(d, size=16, weight=ft.FontWeight.BOLD),
                        width=100,
                        alignment=ft.alignment.center
                    ) for d in days_of_week],
                    alignment=ft.MainAxisAlignment.CENTER
                )
                weeks.append(header)
                
                # Agregar las semanas
                for week in cal:
                    week_row = ft.Row(
                        [build_desktop_day(day) if day != 0 else ft.Container(width=100) for day in week],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                    weeks.append(week_row)
                
                return ft.Column(weeks, scroll=ft.ScrollMode.AUTO)

        # Contenedor principal
        calendar_view = ft.Container(
            content=build_calendar(),
            padding=10,
        )

        def page_resize(e):
            calendar_view.content = build_calendar(e)
            self.update()

        self.page.on_resize = page_resize

        return ft.Column([
            tabs,
            month_title,
            calendar_view
        ])

def main(page: ft.Page):
    page.title = "Voluntarios"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Configuración responsive
    page.window_resizable = True
    page.window_width = 1000
    page.window_height = 800
    page.update()
    
    calendar = VolunteerCalendar()
    page.add(calendar)

if __name__ == "__main__":
    ft.app(target=main)