import flet as ft
from datetime import datetime, timedelta
import locale

class CalendarioVoluntarios(ft.UserControl):
    def __init__(self):
        super().__init__()
        #self.current_date = datetime(2024, 12, 1)
        self.current_date = datetime.now()
        self.days_of_week = ["L", "M", "X", "J", "V", "S", "D"]
        self.shifts = [["T1", "T2"], ["T3", "T4"]]
        self.selected_shifts = {}
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

    def build(self):
        self.month_year = ft.Text(self.current_date.strftime("%B %Y").capitalize(), size=28, weight=ft.FontWeight.BOLD)
        self.calendar_grid = ft.Column(spacing=10, alignment=ft.MainAxisAlignment.CENTER)

        header = ft.Row([
            ft.Container(
                ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=self.previous_month, icon_size=30),
                width=110,
                alignment=ft.alignment.center
            ),
            ft.Container(
                self.month_year,
                expand=True,
                alignment=ft.alignment.center
            ),
            ft.Container(
                ft.IconButton(icon=ft.icons.ARROW_FORWARD, on_click=self.next_month, icon_size=30),
                width=110,
                alignment=ft.alignment.center
            ),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        return ft.Container(
            ft.Column([
                header,
                self.create_calendar()
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            padding=20,
            border_radius=15,
            bgcolor=ft.colors.WHITE,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.colors.BLUE_GREY_300,
                offset=ft.Offset(0, 5),
            )
        )

    def create_calendar(self):
        self.calendar_grid.controls.clear()
        
        # Añadir encabezados de días de la semana
        week_header = ft.Row(spacing=10, alignment=ft.MainAxisAlignment.CENTER)
        for day in self.days_of_week:
            week_header.controls.append(
                ft.Container(
                    ft.Text(day, size=18, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                    width=110,
                    height=40,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.BLUE_400,
                    border_radius=10,
                )
            )
        self.calendar_grid.controls.append(week_header)
        
        # Generar días del mes
        month_days = self.get_month_days()
        for i in range(0, len(month_days), 7):
            week = ft.Row(spacing=10, alignment=ft.MainAxisAlignment.CENTER)
            for day in month_days[i:i+7]:
                if day:
                    day_container = self.create_day_container(day)
                else:
                    day_container = ft.Container(width=110, height=110)
                week.controls.append(day_container)
            self.calendar_grid.controls.append(week)
        
        return self.calendar_grid

    def create_day_container(self, day):
        shifts_column = ft.Column(spacing=2, alignment=ft.MainAxisAlignment.CENTER)
        for shift_row in self.shifts:
            shift_row_container = ft.Row(
                spacing=0,
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True
            )
            for shift in shift_row:
                checkbox = ft.Checkbox(
                    label=shift,
                    value=self.selected_shifts.get(f"{self.current_date.year}-{self.current_date.month}-{day}", {}).get(shift, False),
                    on_change=lambda e, d=day, s=shift: self.toggle_shift(e, d, s),
                    scale=0.8,
                    label_style=ft.TextStyle(size=14),
                )
                shift_row_container.controls.append(checkbox)
            shifts_column.controls.append(shift_row_container)

        return ft.Container(
            ft.Column([
                ft.Text(str(day), size=18, weight=ft.FontWeight.BOLD),
                shifts_column
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
            width=110,
            height=110,
            border=ft.border.all(1, ft.colors.BLUE_GREY_200),
            border_radius=10,
            padding=5,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.WHITE,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=3,
                color=ft.colors.BLUE_GREY_100,
                offset=ft.Offset(0, 2),
            )
        )

    def get_month_days(self):
        first_day = self.current_date.replace(day=1)
        days_before = (first_day.weekday() - 0) % 7
        days_after = 42 - (days_before + self.get_days_in_month(self.current_date.year, self.current_date.month))
        
        days = [None] * days_before + list(range(1, self.get_days_in_month(self.current_date.year, self.current_date.month) + 1)) + [None] * days_after
        return days[:42]

    @staticmethod
    def get_days_in_month(year, month):
        if month == 12:
            next_month = datetime(year + 1, 1, 1)
        else:
            next_month = datetime(year, month + 1, 1)
        return (next_month - timedelta(days=1)).day

    def toggle_shift(self, e, day, shift):
        key = f"{self.current_date.year}-{self.current_date.month}-{day}"
        if key not in self.selected_shifts:
            self.selected_shifts[key] = {}
        self.selected_shifts[key][shift] = e.control.value
        print(f"Turno {shift} para el día {day} {'seleccionado' if e.control.value else 'deseleccionado'}")

    def previous_month(self, e):
        self.current_date = (self.current_date.replace(day=1) - timedelta(days=1)).replace(day=1)
        self.update_calendar()

    def next_month(self, e):
        self.current_date = (self.current_date.replace(day=28) + timedelta(days=4)).replace(day=1)
        self.update_calendar()

    def update_calendar(self):
        self.month_year.value = self.current_date.strftime("%B %Y").capitalize()
        self.create_calendar()
        self.update()

def main(page: ft.Page):
    page.title = "Calendario de Voluntarios"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.colors.BLUE_GREY_50
    calendar = CalendarioVoluntarios()
    page.add(calendar)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)