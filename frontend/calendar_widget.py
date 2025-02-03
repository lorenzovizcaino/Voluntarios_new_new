"""
Módulo que implementa un widget de calendario personalizado para Flet.
Proporciona una interfaz gráfica para seleccionar fechas con soporte para español
"""

import flet as ft
import datetime
import calendar
import locale

class SpanishCalendar(ft.UserControl):
    """
    Widget personalizado que implementa un calendario en español.
    
    Args:
        on_date_selected (callable, optional): Callback para cuando se selecciona una fecha
        on_change (callable, optional): Callback para cuando cambia el estado del calendario
        selected_date (str/datetime, optional): Fecha inicial seleccionada
    
    El calendario soporta navegación entre meses, selección de fechas,
    y múltiples formatos de visualización.
    """

    def __init__(self, on_date_selected=None, on_change=None, selected_date=None):
        super().__init__()
        self.current_date = datetime.datetime.now()
        self.selected_date = None
        self.on_date_selected = on_date_selected
        self.on_change = on_change

        # Intentar establecer el locale en español
        try:
            locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
        except:
            try:
                locale.setlocale(locale.LC_ALL, 'Spanish')
            except:
                print("No se pudo establecer el locale en español")

        # Si se proporciona una fecha inicial, la establecemos
        if selected_date:
            self.set_selected_date(selected_date)


    def set_selected_date(self, date):
        """
        Establece la fecha seleccionada y actualiza la vista del calendario.
        
        Args:
            date: Puede ser un string en formato 'YYYY-MM-DD' o un objeto datetime.date
            
        Raises:
            ValueError: Si el formato de fecha no es válido
            
        Efectos:
            - Actualiza la fecha seleccionada
            - Actualiza la visualización del calendario
        """
        if isinstance(date, str):
            try:
                date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError("La fecha debe estar en formato 'YYYY-MM-DD'")
        elif isinstance(date, datetime.datetime):
            date = date.date()
        elif not isinstance(date, datetime.date):
            raise ValueError("La fecha debe ser un string 'YYYY-MM-DD' o un objeto datetime.date")

        self.selected_date = date
        self.current_date = datetime.datetime(date.year, date.month, 1)
        
        # Si el control ya está construido, actualizamos la vista
        if hasattr(self, 'selected_date_text'):
            self.selected_date_text.value = f"Fecha seleccionada: {self.selected_date.strftime('%d de %B de %Y')}"
            self.month_text.value = self.current_date.strftime("%B %Y").capitalize()
            self.calendar_container.content = self.create_calendar_grid(
                self.current_date.year,
                self.current_date.month
            )
            self.update()







    def create_calendar_grid(self, year, month):
        """
        Crea la cuadrícula del calendario para un mes específico.
        
        Args:
            year (int): Año a mostrar
            month (int): Mes a mostrar
            
        Returns:
            ft.Column: Contenedor con la cuadrícula del calendario
        """

        cal = calendar.monthcalendar(year, month)
        days_header = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
        header_row = ft.Row(
            controls=[ft.Text(day, size=14, width=40, text_align="center") for day in days_header],
            alignment=ft.MainAxisAlignment.CENTER
        )

        def day_clicked(day):
            """
            Crea un manejador de eventos para la selección de un día.
            
            Args:
                day (int): Día seleccionado
                
            Returns:
                callable: Función manejadora del evento
            """
            def handle_click(e):
                old_date = self.selected_date
                self.selected_date = datetime.date(year, month, day)
                self.selected_date_text.value = f"Fecha seleccionada: {self.selected_date.strftime('%d de %B de %Y')}"
                
                # Llamar a on_date_selected si existe
                if self.on_date_selected:
                    self.on_date_selected(self.get_selected_date())
                
                # Llamar a on_change si existe y la fecha ha cambiado
                if self.on_change and old_date != self.selected_date:
                    self.on_change({
                        'old_date': old_date,
                        'new_date': self.selected_date,
                        'old_data': self.format_date_data(old_date) if old_date else None,
                        'new_data': self.get_selected_date()
                    })
                
                # Actualizar el estilo del botón seleccionado
                self.reset_calendar()
                for row in self.calendar_rows:
                    for btn in row.controls:
                        if isinstance(btn, ft.ElevatedButton) and btn.text == str(day):
                            btn.style = ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=5),
                                padding=0,
                                bgcolor=ft.colors.GREEN_200
                            )
                self.update()
            return handle_click

        # Crear cuadrícula de días
        self.calendar_rows = []
        for week in cal:
            week_buttons = []
            for day in week:
                if day == 0:
                    btn = ft.Container(width=40, height=40)
                else:

                    # Verificamos si este día es el seleccionado
                    is_selected = (self.selected_date and 
                                 self.selected_date.year == year and 
                                 self.selected_date.month == month and 
                                 self.selected_date.day == day)


                    btn = ft.ElevatedButton(
                        text=str(day),
                        width=40,
                        height=40,
                        on_click=day_clicked(day),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=5),
                            padding=0,
                            bgcolor=ft.colors.GREEN_200 if is_selected else None
                        )
                    )
                week_buttons.append(btn)
            
            self.calendar_rows.append(
                ft.Row(controls=week_buttons, alignment=ft.MainAxisAlignment.CENTER)
            )

        return ft.Column(
            controls=[header_row] + self.calendar_rows,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def format_date_data(self, date):
        """
        Formatea una fecha en un diccionario con múltiples formatos.
        
        Args:
            date (datetime.date): Fecha a formatear
            
        Returns:
            dict: Diccionario con diferentes representaciones de la fecha
        """
        if date is None:
            return None
            
        return {
            'date': date,
            'day': date.day,
            'month': date.month,
            'year': date.year,
            'month_name': date.strftime('%B').capitalize(),
            'formatted': date.strftime('%d/%m/%Y'),
            'iso': date.strftime('%Y-%m-%d')
        }

    def change_month(self, delta):
        """
        Crea un manejador para cambiar el mes mostrado.
        
        Args:
            delta (int): Cantidad de meses a avanzar/retroceder
            
        Returns:
            callable: Función manejadora del evento
        """
        def handle_change(e):
            old_date = self.current_date
            self.current_date = self.current_date.replace(day=1)
            self.current_date = self.current_date + datetime.timedelta(days=32 * delta)
            self.current_date = self.current_date.replace(day=1)
            
            # Llamar a on_change si existe y el mes ha cambiado
            if self.on_change and (old_date.month != self.current_date.month or 
                                 old_date.year != self.current_date.year):
                self.on_change({
                    'type': 'month_change',
                    'old_month': old_date.month,
                    'new_month': self.current_date.month,
                    'old_year': old_date.year,
                    'new_year': self.current_date.year
                })
            
            # Actualizar vista
            self.month_text.value = self.current_date.strftime("%B %Y").capitalize()
            self.calendar_container.content = self.create_calendar_grid(
                self.current_date.year, 
                self.current_date.month
            )
            self.update()
        return handle_change

    def reset_calendar(self):
        """
        Reinicia el calendario a su estado inicial.
        Elimina la selección actual y actualiza la vista.
        """
        old_date = self.selected_date
        for row in self.calendar_rows:
            for btn in row.controls:
                if isinstance(btn, ft.ElevatedButton):
                    btn.style = ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=5),
                        padding=0,
                        bgcolor=None
                    )
        self.selected_date = None
        self.selected_date_text.value = ""
        
        # Llamar a on_change si existe y había una fecha seleccionada
        if self.on_change and old_date is not None:
            self.on_change({
                'type': 'reset',
                'old_date': old_date,
                'new_date': None,
                'old_data': self.format_date_data(old_date),
                'new_data': None
            })
            
        self.update()

    def build(self):
        """
        Construye la interfaz del calendario.
        
        Returns:
            ft.Container: Contenedor principal del calendario
        """
        # Título del mes actual
        self.month_text = ft.Text(
            self.current_date.strftime("%B %Y").capitalize(),
            size=20,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )

        # Barra de navegación
        navigation = ft.Row(
            controls=[
                ft.IconButton(ft.icons.ARROW_LEFT, on_click=self.change_month(-1)),
                self.month_text,
                ft.IconButton(ft.icons.ARROW_RIGHT, on_click=self.change_month(1))
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

        # Texto de fecha seleccionada
        self.selected_date_text = ft.Text(size=16, text_align=ft.TextAlign.CENTER)
        
        # Contenedor del calendario
        self.calendar_container = ft.Container(
            content=self.create_calendar_grid(self.current_date.year, self.current_date.month),
            padding=10
        )

        # Contenedor principal
        return ft.Container(
            content=ft.Column(
                controls=[
                    navigation,
                    self.calendar_container,
                    self.selected_date_text
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=20
        )

    def get_selected_date(self):
        """
        Obtiene la fecha seleccionada en múltiples formatos.
        
        Returns:
            dict: Diccionario con la fecha separada en diferentes formatos:
                - date: objeto datetime.date
                - day: día del mes (1-31)
                - month: mes (1-12)
                - year: año (YYYY)
                - month_name: nombre del mes en español
                - formatted: fecha formateada (DD/MM/YYYY)
                - iso: fecha en formato ISO (YYYY-MM-DD)
        """
        if self.selected_date is None:
            return None
            
        return {
            'date': self.selected_date,
            'day': self.selected_date.day,
            'month': self.selected_date.month,
            'year': self.selected_date.year,
            'month_name': self.selected_date.strftime('%B').capitalize(),
            'formatted': self.selected_date.strftime('%d/%m/%Y'),
            'iso': self.selected_date.strftime('%Y-%m-%d')
        }