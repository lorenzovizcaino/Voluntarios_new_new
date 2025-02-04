"""
Módulo que implementa la vista de usuario del sistema.
Proporciona funcionalidades para:
- Visualización de tareas asignadas
- Gestión de disponibilidad mediante diferentes vistas de calendario
- Configuración de turnos y preferencias
"""

import os
import flet as ft
import requests
import calendar
from datetime import datetime, timedelta

from utils import (
    API_URL_TURNOS, get_id_usuario_logeado, API_URL_LOGIN,
    API_URL_TAREAS_ASIGNADAS, API_URL_TAREAS, path_fondo
)

def user(page: ft.Page):
    """
    Implementa la vista principal del usuario.
    
    Args:
        page (ft.Page): Objeto page de Flet
        
    Returns:
        ft.View: Vista principal con pestañas para diferentes funcionalidades
    """
    # Configuración inicial de la ventana
    page.window_width = 1000
    page.window_height = 1000  
    page.window_center()
    page.bgcolor = ft.colors.TRANSPARENT
    page.window_bgcolor = ft.colors.TRANSPARENT

    # Variables de control para navegación entre meses
    comprobar_mes = 0
    comprobar_mes2 = 0
    comprobar_mes3 = 0
    today = datetime.now()
    valor_checkbox = False
    lista_estado_checkbox=[]

    
    
    # Elementos de interfaz para encabezados de calendario
    calendar_header = ft.Text("", weight="bold", size=30)
    calendar_header2 = ft.Text("", weight="bold", size=30)
    calendar_header3 = ft.Text("", weight="bold", size=30)

    # Leyendas explicativas de turnos
    leyenda=ft.Text(value="T1: de 09:00 a 12:00       T2: de 12:00 a 15:00        T3: de 15:00 a 18:00        T4: de 18:00 a 21:00",
                        size=15,
                        weight=ft.FontWeight.BOLD)
    leyenda2=ft.Text(value="Turno 1: de 09:00 a 12:00       Turno 2: de 12:00 a 15:00        Turno 3: de 15:00 a 18:00        Turno 4: de 18:00 a 21:00",
                        size=15,
                        weight=ft.FontWeight.BOLD)
    leyendaTelegram=ft.Text(value='Si quiere recibir un mensaje el dia anterior a una tarea: buscar en Telegram el canal  "Voluntarios", ponga su telefono y envie',
                        size=14,
                        color="GREEN",
                        weight=ft.FontWeight.BOLD)
    
    # Diccionario para traducción de meses
    meses = {
                    'January': 'Enero',
                    'February': 'Febrero',
                    'March': 'Marzo',
                    'April': 'Abril',
                    'May': 'Mayo',
                    'June': 'Junio',
                    'July': 'Julio',
                    'August': 'Agosto',
                    'September': 'Septiembre',
                    'October': 'Octubre',
                    'November': 'Noviembre',
                    'December': 'Diciembre'
                }


    def mostrar_mes():
        """
        Calcula y muestra el mes correspondiente según el índice actual.
        
        Returns:
            datetime: Fecha del mes a mostrar
            
        Efectos:
            - Actualiza el texto del encabezado del calendario
        """

        nonlocal comprobar_mes        
        # Calcular el mes objetivo
        target_date = today.replace(day=1)
        for _ in range(comprobar_mes):
            target_date = (target_date.replace(day=1) + timedelta(days=32)).replace(day=1)

        next_month = target_date
        # Actualizar el texto del encabezado
        mes=next_month.strftime('%B')
        anho=next_month.strftime('%Y')
        
        calendar_header.value = f"{meses[mes]} {anho}"        
        return next_month
    
    




    #PESTAÑA CALENDARIO POR DIA INDIVIDUAL
    lista_para_tabla = []





    
    def montar_calendario():
        """
        Construye la interfaz del calendario por día.
        
        Construye una cuadrícula que muestra:
        - Encabezados de días de la semana
        - Casillas para cada día del mes
        - Checkboxes de turnos para cada día
                
        Efectos:
            - Actualiza columna_calendario_disponibilidad con el nuevo calendario
        """
        nonlocal comprobar_mes, calendar_header
        check_deshabilitado=False
        next_month = mostrar_mes()
        
        if next_month.month==today.month:
            check_deshabilitado=True



        days_of_week = ["L", "M", "X", "J", "V", "S", "D"]
        turnos = ["T1", "T2", "T3", "T4"]
        
        # Constantes para dimensiones 
        CELL_WIDTH = 20 * 4 + 20
        CELL_SPACING = 8
        ROW_WIDTH = (CELL_WIDTH * 7) + (CELL_SPACING * 6)
        
        
        
        # Crear encabezado con días de la semana
        header_row = ft.Container(
            ft.Row(
                [
                    ft.Container(
                        ft.Text(
                            day,
                            weight="bold",
                            size=35,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        width=CELL_WIDTH,
                        height=45,
                        alignment=ft.alignment.center,
                        border=ft.border.all(color=ft.colors.TRANSPARENT),
                    ) 
                    for day in days_of_week
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=CELL_SPACING,
                width=ROW_WIDTH,
            ),
            alignment=ft.alignment.center,
            width=ROW_WIDTH,
        )

        # Generar la cuadrícula de días
        first_day = next_month
        start_day = first_day - timedelta(days=first_day.weekday())
        days_grid = []

        for week in range(6):
            row_cells = []
            for day in range(7):
                current_day = start_day + timedelta(days=week * 7 + day)
                
                # Crear fila de turnos
                turnos_row = ft.Row(
                    [ft.Text(value=f"{turno}", width=20, height=18, size=13) for turno in turnos] if current_day.month == next_month.month else [ft.Text(value="", width=20, height=18) for _ in turnos],
                    alignment="center",
                    spacing=2,
                )         
                
                # Crear checkboxes de turnos
                checkboxes = []            
                if current_day.month == next_month.month:  
                    year = current_day.year
                    month = current_day.month
                    day = current_day.day
                                
                    for ch in range(4):                                            
                        try:
                            # Verificar estado del turno en la base de datos
                            params = {
                                "user_id": get_id_usuario_logeado(),
                                "year": year, 
                                "month": month, 
                                "day": day, 
                                "checkbox": ch
                            }               
                            response = requests.get(API_URL_TURNOS, params=params)             
                            valor_checkbox = response.status_code == 200
                        except Exception as e:
                            print(f"Error al obtener datos: {str(e)}")
                            valor_checkbox = False

                        checkboxes.append(ft.Checkbox(
                            label="",
                            value=valor_checkbox, 
                            width=20, 
                            key={"ch":ch,"current_day":current_day},
                            height=18,
                            disabled=check_deshabilitado,
                            on_change=modificar_tabla
                        ))
                else:
                    checkboxes = [ft.Container(width=20, height=18) for _ in range(4)]
                
                checkboxes_row = ft.Row(
                    checkboxes,        
                    alignment="center", 
                    spacing=2          
                )              

                # Configurar texto del día                  
                day_text = ft.Container(
                    ft.Text(
                        str(current_day.day) if current_day.month == next_month.month else "",
                        text_align=ft.TextAlign.CENTER,
                        size=35  
                    ),
                    alignment=ft.alignment.center,
                    width=CELL_WIDTH,
                )
                
                # Crear celda completa del día
                day_cell = ft.Container(
                    content=ft.Column(
                        [
                            day_text,
                            turnos_row,
                            checkboxes_row
                        ],
                        spacing=3,  
                        alignment="center",
                        width=CELL_WIDTH,
                        height=100,  
                    ),
                    border=ft.border.all(color=ft.colors.BLACK, width=2) if current_day.month == next_month.month else ft.border.all(color=ft.colors.TRANSPARENT),
                    bgcolor="#eed8cc" if current_day.month == next_month.month else ft.colors.TRANSPARENT,
                    border_radius=5,
                    width=CELL_WIDTH,
                    
                )
                
                row_cells.append(day_cell)
                
            # Crear fila de la semana
            calendar_row = ft.Row(
                row_cells, 
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=CELL_SPACING,
                width=ROW_WIDTH,
            )
            days_grid.append(calendar_row)

        # Contenedor principal del calendario
        calendar_container = ft.Container(
            content=ft.Column(
                [
                    ft.Container(height=20),
                    fila_header,
                    header_row,
                    ft.Container(height=5),
                    *days_grid,
                    leyenda
            
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
        )

        columna_calendario_disponibilidad.controls = [calendar_container]
    
    
    
    
    def modificar_tabla(e):
        """
        Maneja los cambios en los checkboxes de disponibilidad.
        
        Args:
            e: Evento del checkbox que incluye la información del día y turno modificado
            
        Efectos:
            - Actualiza la disponibilidad en la base de datos
            - Refresca todas las vistas de calendario
        """

        if e and e.control and e.control.key:
            year = e.control.key["current_day"].year
            month = e.control.key["current_day"].month
            day = e.control.key["current_day"].day
            ch = e.control.key["ch"]
            
            data = {
                "user_id": get_id_usuario_logeado(), 
                "year": year, 
                "month": month, 
                "day": day, 
                "turno1": ch == 0, 
                "turno2": ch == 1, 
                "turno3": ch == 2, 
                "turno4": ch == 3
            }
            
            try:
                if e.control.value:       
                    response = requests.post(API_URL_TURNOS, json=data)
                else:
                    response = requests.delete(API_URL_TURNOS, json=data)

                # Actualizar todas las pestañas después de cada cambio
                mostrar_mes2()
                columna_de_tab2.controls[1] = montar_calendario_por_turno()
                mostrar_mes3()
                columna_de_tab3.controls[1] = montar_calendario_por_dias_semana()
                page.update()


            except Exception as e:
                print(f"Error al modificar turno: {str(e)}")

    
    def actualizar_estado_botones():
        """Actualiza el estado habilitado/deshabilitado de los botones de navegación."""
        flecha_izquierda.content.disabled = comprobar_mes == 0
        flecha_derecha.content.disabled = comprobar_mes == 2

    
    
    def mes_menos(e):
        """Navega al mes anterior si está permitido."""
        nonlocal comprobar_mes
        if comprobar_mes > 0:
            comprobar_mes -= 1
            
            actualizar_estado_botones()
            montar_calendario()    
        
        page.update()

    def mes_mas(e):
        """Navega al mes siguiente si está permitido."""
        nonlocal comprobar_mes
        if comprobar_mes < 2:
            comprobar_mes += 1    
                       
            actualizar_estado_botones()
            montar_calendario()
        
        page.update()

    # Configuración de botones de navegación
    flecha_izquierda = ft.Container(
        content=ft.IconButton(
            icon=ft.icons.ARROW_CIRCLE_LEFT, 
            icon_size=40,                              
            on_click=mes_menos,
            icon_color=ft.colors.BLUE_800 ,
            disabled= True
        )
    )  

    flecha_derecha = ft.Container(
        content=ft.IconButton(
            icon=ft.icons.ARROW_CIRCLE_RIGHT, 
            icon_size=40,
            on_click=mes_mas,
            icon_color=ft.colors.BLUE_800 ,
            disabled= False
        )
    )

    fila_header = ft.Row(
        controls=[flecha_izquierda, calendar_header, flecha_derecha],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15
    )
    
    # Crear la columna principal del calendario
    columna_calendario_disponibilidad = ft.Column(
        [],  # Inicialmente vacío, se llenará en montar_calendario()
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    
    montar_calendario()
    


    #CONTENIDO DE LA PESTAÑA VER TAREAS


    def obtener_nombre_usuario():
        """
        Obtiene el nombre del usuario actual desde la API.
        
        Returns:
            str: Nombre de usuario o None si hay error
        """
        try:
                
            response=requests.get(f"{API_URL_LOGIN}/{get_id_usuario_logeado()}")
            if response.status_code==200:                    
                data = response.json()
                nombre_usuario_logeado=data["username"]
                return nombre_usuario_logeado
                

                
            else:
                print(f"Error al obtener datos: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error en la conexión: {str(e)}")
            return None

    def logout(e):
        """Redirige a la página de login."""
        page.go("/login")

    def cargar_datos():
        """
        Carga las tareas asignadas al usuario actual.
        
        Returns:
            list: Lista de tareas completas o None si hay error
        """
        id_tareas_usuario=[]
        tareas_usuario=[]        
        #Se recuperan todas las tareas del usuario por su id
        try:
            response=requests.get(f"{API_URL_TAREAS_ASIGNADAS}/{get_id_usuario_logeado()}")
            if response.status_code==200:
                data = response.json()
                task = data["tareas"] 
                for tarea in task:
                    id_tareas_usuario.append(tarea["tarea_id"])
                
            else:
                print(f"Error al obtener datos: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error en la conexión: {str(e)}")
            return None
        
        #Se recuperan las tareas completas por el id recuperado en el bloque anterior
        for id_tarea in id_tareas_usuario:
            try:
                response=requests.get(f"{API_URL_TAREAS}/{id_tarea}")
                if response.status_code==200:                    
                    data = response.json()
                    tareas_usuario.append(data)      
                else:
                    print(f"Error al obtener datos: {response.status_code}")
                    return None
                
            except Exception as e:
                print(f"Error en la conexión: {str(e)}")
                return None
            
        return tareas_usuario
        


    def crear_tabla_tareas_usuarios():
        """
        Crea la tabla de tareas asignadas al usuario.
        Actualiza lista_para_tabla con los datos obtenidos.
        """
        lista_base_datos=cargar_datos()
        lista_para_tabla.clear()
        for tarea in lista_base_datos:
            id=tarea["id"]
            nombre=tarea["tarea_name"]
            ubicacion=tarea["tarea_ubicacion"]
            fecha=f"{tarea["day"]}/{tarea["month"]}/{tarea["year"]}"
            turno=tarea["turno"]
            v_necesarios=tarea["voluntarios_necesarios"]
            v_asignados=tarea["voluntarios_asignados"]
            lista_para_tabla.append({"id":id,"nombre":nombre, "ubicacion":ubicacion,"fecha":fecha,"turno":turno,"voluntarios_necesarios":v_necesarios,"voluntarios_asignados":v_asignados})
        actualizar_tabla()

            
    def actualizar_tabla():
        """
        Actualiza la visualización de la tabla de tareas.
        Limpia y reconstruye las filas con los datos actuales.
        """
        data_table.rows.clear()

        for dato in lista_para_tabla:
            
            data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(dato["nombre"], size=16, ), 
                                padding=ft.padding.all(5),
                                alignment=ft.alignment.center_left
                                
                                
                            )
                        ),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(dato["ubicacion"], size=16, ), 
                                padding=ft.padding.all(5),
                                alignment=ft.alignment.center_left
                                
                                
                            )
                        ),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(dato["fecha"], size=16, ),
                                padding=ft.padding.all(5),
                                alignment=ft.alignment.center
                            )
                        ),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(dato["turno"], size=16, ),
                                padding=ft.padding.all(5),
                                alignment=ft.alignment.center
                            )
                        ),
                        ft.DataCell(
                            
                            ft.Container(
                                content=ft.Text(str(dato["voluntarios_necesarios"]), size=16, ),
                                padding=ft.padding.all(5),
                                alignment=ft.alignment.center
                                
                            )
                        ),


                        
                    ]
                )
            )
        page.update()



    # Configuración de elementos de interfaz para el encabezado
    usuario = ft.Text(value=obtener_nombre_usuario(), size=23, color=ft.colors.BLUE_800)
    icono_logout = ft.IconButton(icon=ft.icons.LOGOUT, icon_size=25, on_click=logout, icon_color=ft.colors.BLUE_800)
    fila_encabezado = ft.Row(
        controls=[usuario, icono_logout],
        alignment=ft.MainAxisAlignment.END,  # Alinea horizontalmente a la derecha
        vertical_alignment=ft.CrossAxisAlignment.START  # Alinea verticalmente arriba
    )




    
    # Configuración de la tabla de datos
    data_table = ft.DataTable(    
            
        #bgcolor=ft.colors.with_opacity(0.8, "#eed8cc"),
        bgcolor="#eed8cc",
        border=ft.border.all(width=3, color=ft.colors.WHITE),
        border_radius=8,       
        #vertical_lines=ft.border.BorderSide(1, ft.colors.BLUE_GREY_50),
        horizontal_lines=ft.border.BorderSide(2, ft.colors.WHITE),  
         
    
        columns=[            
            ft.DataColumn(
                label=ft.Container(
                    content=ft.Text(
                        "Tarea",
                        color=ft.colors.BLUE_GREY_800,
                        size=16,
                        weight=ft.FontWeight.W_500,
                        text_align=ft.TextAlign.CENTER,
                        
                    ),
                    alignment=ft.alignment.center,
                    width=200
                ),
                numeric=False,
            ),
            ft.DataColumn(
                label=ft.Container(
                    content=ft.Text(
                        "Ubicación",
                        color=ft.colors.BLUE_GREY_800,
                        size=16,
                        weight=ft.FontWeight.W_500,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    width=200
                ),
                numeric=False,
            ),
            ft.DataColumn(
                label=ft.Container(
                    content=ft.Text(
                        "Fecha",
                        color=ft.colors.BLUE_GREY_800,
                        size=16,
                        weight=ft.FontWeight.W_500,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    width=80
                ),
                numeric=False,
            ),
            ft.DataColumn(
                label=ft.Container(
                    content=ft.Text(
                        "Turno",
                        color=ft.colors.BLUE_GREY_800,
                        size=16,
                        weight=ft.FontWeight.W_500,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    width=80
                    
                ),
                numeric=False,
            ),
            ft.DataColumn(
                label=ft.Container(
                    content=ft.Text(
                        "Voluntarios necesarios",
                        color=ft.colors.BLUE_GREY_800,
                        size=16,
                        weight=ft.FontWeight.W_500,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    width=90
                    
                ),
                numeric=True,
            ),
            
        ],
        
        
        heading_row_height=50,
        data_row_min_height=45,
        data_row_max_height=60,
        column_spacing=20,
        
        
        
        
        rows=[]
    )

    # Contenedor para la tabla con scroll
    tabla_con_scroll = ft.ListView(
        controls=[data_table],
        expand=1,
        height=400, 
    )

    contenedor_tabla = ft.Container(
        content=tabla_con_scroll,
        width=850,        
        border_radius=8,
        padding=0,
        
    )    



    crear_tabla_tareas_usuarios()

    # Columna principal para tareas asignadas
    columna_tareas_asignadas=ft.Column(controls=[
            
            fila_encabezado,  
            ft.Container(height=80),           
            contenedor_tabla, 
            ft.Container(height=240),
            leyenda2,
            leyendaTelegram,
            
            ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    

    #PESTAÑA CALENDARIO POR TURNOS


    def mostrar_mes2():
        """
        Controla la visualización del mes para la vista de calendario por turnos.
        Actualiza el encabezado con el mes y año correspondiente.
        """
        nonlocal comprobar_mes2        
        # Calcular el mes objetivo
        target_date = today.replace(day=1)
        for _ in range(comprobar_mes2):
            target_date = (target_date.replace(day=1) + timedelta(days=32)).replace(day=1)

        next_month = target_date
        # Actualizar el texto del encabezado
        mes=next_month.strftime('%B')
        anho=next_month.strftime('%Y')               
        calendar_header2.value = f"{meses[mes]} {anho}"
        return next_month

    def actualizar_estado_botones2():
        """ Actualizar estado de los botones según comprobar_mes """
        flecha_izquierda2.content.disabled = comprobar_mes2 == 0
        flecha_derecha2.content.disabled = comprobar_mes2 == 2

    
    
    def mes_menos2(e):
        """Navega al mes anterior si es posible."""
        nonlocal comprobar_mes2
        if comprobar_mes2 > 0:
            comprobar_mes2 -= 1
            columna_de_tab2.controls[1] = montar_calendario_por_turno()
            actualizar_estado_botones2()                
            page.update()

    def mes_mas2(e):
        """Navega al mes siguiente si es posible."""
        nonlocal comprobar_mes2
        if comprobar_mes2 < 2:
            comprobar_mes2 += 1    
            columna_de_tab2.controls[1] = montar_calendario_por_turno()         
            actualizar_estado_botones2()                   
            page.update()

    def cambiar_turnos(e):
        """
        Gestiona cambios en los turnos para todo un mes.
        
        Args:
            e: Evento del checkbox con información del turno seleccionado
            
        Efectos:
            - Actualiza la disponibilidad para todo el mes en la base de datos
            - Refresca todas las vistas de calendario
        """
        user_id=get_id_usuario_logeado()
        month=mostrar_mes2().month
        year=mostrar_mes2().year
        ch=e.control.key["ch"]
        
        
        # metodo que obtiene el numero de dias de un mes y año especificado
        num_dias = calendar.monthrange(year, month)[1]  
    
        for day in range(1, num_dias + 1):
            data = {
                "user_id": get_id_usuario_logeado(), 
                "year": year, 
                "month": month, 
                "day": day, 
                "turno1": ch == 0, 
                "turno2": ch == 1, 
                "turno3": ch == 2, 
                "turno4": ch == 3
            }

            params = {
                        "user_id": get_id_usuario_logeado(),
                        "year": year, 
                        "month": month, 
                        "day": day, 
                        "checkbox": ch
                    } 

            try:
                if e.control.value:   
                    response = requests.get(API_URL_TURNOS, params=params)   
                    if response.status_code != 200:
                        requests.post(API_URL_TURNOS, json=data)
                else:
                    requests.delete(API_URL_TURNOS, json=data)

                # Actualizar todas las pestañas después de cada cambio
                montar_calendario()
                columna_de_tab3.controls[1] = montar_calendario_por_dias_semana()
                page.update()


            except Exception as e:
                print(f"Error al modificar turno: {str(e)}")
        

        

    def montar_calendario_por_turno():
        """
        Construye la interfaz de calendario por turnos.
        Permite seleccionar disponibilidad para un turno específico en todo el mes.
        
        Returns:
            ft.Container: Contenedor con la interfaz de turnos mensuales
        """
        check_deshabilitado=False
        checkboxes = []
        user_id=get_id_usuario_logeado()
        month=mostrar_mes2().month
        year=mostrar_mes2().year

        if month==today.month:
            check_deshabilitado=True

        
        # metodo que obtiene el numero de dias de un mes y año especificado
        num_dias = calendar.monthrange(year, month)[1] 
        for ch in range(4):
            valor_checkbox = True
            for day in range(1, num_dias + 1): 
                try:
                    params = {
                        "user_id": user_id,
                        "year": year, 
                        "month": month, 
                        "day": day, 
                        "checkbox": ch
                    }               
                    response = requests.get(API_URL_TURNOS, params=params)             
                    
                    if response.status_code != 200:
                        valor_checkbox=False
                        break
                except Exception as e:
                        print(f"Error al obtener datos: {str(e)}")
                        valor_checkbox = False

            checkboxes.append(ft.Checkbox(
                            label="",
                            value=valor_checkbox, 
                            scale=1.3, 
                            key={"ch":ch},
                            height=18,
                            disabled=check_deshabilitado,
                            on_change=cambiar_turnos
                        ))
        
        
        # Crear filas para cada turno
        filas_turnos = [
            ft.Row(
                controls=[
                    ft.Text(value=f"Turno {ch}", size=25),
                    checkboxes[ch-1]  
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,  
                #spacing=2  
            ) for ch in range(1,5)
]

        # Contenedor principal de turnos
        fila_por_turnos = ft.Container(
            content=ft.Column(
                controls=filas_turnos,
                spacing=30,  # Espacio entre cada fila de turno
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            #bgcolor=ft.colors.with_opacity(0.8, ft.colors.GREEN_50),
            bgcolor="#eed8cc",
            width=250,
            height=290,
            padding=20, 
            border=ft.border.all(width=2, color=ft.colors.BLACK),
            border_radius=8
        )
















        # Contenedor centrado en la pantalla
        contenedor_centrado = ft.Column(
            controls=[
                ft.Row(
                    controls=[fila_por_turnos],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            ],
            
            expand=True
        )       
        
        return contenedor_centrado
        

    
    flecha_izquierda2 = ft.Container(
        content=ft.IconButton(
            icon=ft.icons.ARROW_CIRCLE_LEFT, 
            icon_size=40,                              
            on_click=mes_menos2,
            icon_color=ft.colors.BLUE_800 ,
            disabled= True
        )
    )  

    flecha_derecha2 = ft.Container(
        content=ft.IconButton(
            icon=ft.icons.ARROW_CIRCLE_RIGHT, 
            icon_size=40,
            on_click=mes_mas2,
            icon_color=ft.colors.BLUE_800 ,
            disabled= False
        )
    )





    fila_header2 = ft.Row(
        controls=[
            ft.Container(height=200),
            flecha_izquierda2,
            calendar_header2, 
            flecha_derecha2],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15, 
        
    )

    columna_por_turnos=montar_calendario_por_turno()

    columna_de_tab2=ft.Column(controls=[
                
                fila_header2,
                columna_por_turnos,
                leyenda2,
                ft.Container(height=20)
                ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            
                
                )


     #PESTAÑA CALENDARIO POR DIAS DE SEMANA

    def mostrar_mes3():
        """Gestiona visualización del mes en vista por días de semana."""
        nonlocal comprobar_mes3        
        # Calcular el mes objetivo
        target_date = today.replace(day=1)
        for _ in range(comprobar_mes3):
            target_date = (target_date.replace(day=1) + timedelta(days=32)).replace(day=1)

        next_month = target_date
        # Actualizar el texto del encabezado
        mes=next_month.strftime('%B')
        anho=next_month.strftime('%Y')               
        calendar_header3.value = f"{meses[mes]} {anho}"
        return next_month

    def actualizar_estado_botones3():
        """Actualiza estado de botones de navegación semanal."""
        flecha_izquierda3.content.disabled = comprobar_mes3 == 0
        flecha_derecha3.content.disabled = comprobar_mes3 == 2

    
    
    def mes_menos3(e):
        """Navega al mes anterior en vista semanal."""
        nonlocal comprobar_mes3
        if comprobar_mes3 > 0:
            comprobar_mes3 -= 1
            columna_de_tab3.controls[1] = montar_calendario_por_dias_semana()
            actualizar_estado_botones3()                
            page.update()

    def mes_mas3(e):
        """Navega al mes siguiente en vista semanal."""
        nonlocal comprobar_mes3
        if comprobar_mes3 < 2:
            comprobar_mes3 += 1    
            columna_de_tab3.controls[1] = montar_calendario_por_dias_semana()         
            actualizar_estado_botones3()                   
            page.update()

    
    
    def montar_calendario_por_dias_semana():
        """
        Construye interfaz de calendario organizada por días de la semana.
        Permite gestionar disponibilidad para todos los turnos de cada día.
        
        Returns:
            ft.Container: Tabla con interfaz de días y turnos
        """
        check_deshabilitado=False
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        turnos = ["Turno 1", "Turno 2", "Turno 3", "Turno 4"]
        dias_semana = {
            'Lunes': [],
            'Martes': [],
            'Miércoles': [],
            'Jueves': [],
            'Viernes': [],
            'Sábado': [],
            'Domingo': []
        }

        user_id=get_id_usuario_logeado()
        month=mostrar_mes3().month
        year=mostrar_mes3().year

        if month==today.month:
            check_deshabilitado=True
        
        def on_checkbox_changed(e, dia_semana, ch):
            """
            Maneja cambios en checkboxes individuales.
            Actualiza disponibilidad para un turno específico en todos los días del tipo seleccionado.
            """
            dias_modificar=[]
            _, num_dias = calendar.monthrange(year, month)

             # Limpiar el diccionario antes de volver a llenarlo
            for dia in dias:
                dias_semana[dia] = []  
            for dia in range(1, num_dias + 1):
                fecha = datetime(year, month, dia)
                # weekday() devuelve 0 para lunes, 1 para martes, etc.
                nombre_dia = dias[fecha.weekday()]
                dias_semana[nombre_dia].append(dia)
            dias_modificar=dias_semana[dia_semana]
            
            
            for day in dias_modificar:
                
                data = {
                        "user_id": user_id, 
                        "year": year, 
                        "month": month, 
                        "day": day, 
                        "turno1": ch == 0, 
                        "turno2": ch == 1, 
                        "turno3": ch == 2, 
                        "turno4": ch == 3
                    }

                params = {
                            "user_id": user_id,
                            "year": year, 
                            "month": month, 
                            "day": day, 
                            "checkbox": ch
                        } 

                try:
                    if e.control.value:   
                        response = requests.get(API_URL_TURNOS, params=params)   
                        if response.status_code != 200:
                            requests.post(API_URL_TURNOS, json=data)
                    else:
                        requests.delete(API_URL_TURNOS, json=data)

                    # Actualizar todas las pestañas después de cada cambio
                    montar_calendario()
                    columna_de_tab2.controls[1] = montar_calendario_por_turno()
                    page.update()


                except Exception as e:
                    print(f"Error al modificar turno: {str(e)}")
            
            columna_de_tab3.controls[1] = montar_calendario_por_dias_semana()
            page.update()


        def on_checkbox_general_changed(e, dia_semana):      
            """Maneja cambios en checkboxes generales que afectan todos los turnos."""    
            for i in range (0,4):                
                on_checkbox_changed(e,dia_semana,i)         
            
            columna_de_tab3.controls[1] = montar_calendario_por_dias_semana()        
            page.update()

        # Crear las columnas de la tabla primero
        columns = [
            ft.DataColumn(
                label=ft.Container(
                    content=ft.Text("Días", weight=ft.FontWeight.BOLD),
                    padding=10,
                )
            )
        ]
        
        # Agregar columnas para cada turno
        for turno in turnos:
            columns.append(
                ft.DataColumn(
                    label=ft.Container(
                        content=ft.Text(turno, weight=ft.FontWeight.BOLD),
                        padding=10,
                    )
                )
            )



        columns.append(
                ft.DataColumn(
                    label=ft.Container(
                        content=ft.Text("Todos Turnos", weight=ft.FontWeight.BOLD),
                        padding=10,
                    )
                )
            )

        # Crear las filas con los checkboxes
        rows = []
        for dia in dias:
            cells = [
                ft.DataCell(
                    ft.Container(
                        content=ft.Text(dia),
                        padding=10,
                    )
                )
            ]
            
            # Agregar checkboxes para cada turno
            for i, turno in enumerate(turnos):


                #comprobar si el checkbox es True o False
                dias_modificar=[]
                _, num_dias = calendar.monthrange(year, month)

                # Limpiar el diccionario antes de volver a llenarlo
                for dia_dicionario in dias:
                    dias_semana[dia_dicionario] = []  
                for dia_mes in range(1, num_dias + 1):
                    fecha = datetime(year, month, dia_mes)
                    # weekday() devuelve 0 para lunes, 1 para martes, etc.
                    nombre_dia = dias[fecha.weekday()]
                    dias_semana[nombre_dia].append(dia_mes)
                dias_modificar=dias_semana[dia]
                
                valor_check=True


                for dia_modificar in dias_modificar:
                    try:
                        params = {
                            "user_id": user_id,
                            "year": year, 
                            "month": month, 
                            "day": dia_modificar, 
                            "checkbox": i
                        }               
                        response = requests.get(API_URL_TURNOS, params=params)             
                        
                        if response.status_code != 200:
                            valor_check=False
                            break
                    except Exception as e:
                            print(f"Error al obtener datos: {str(e)}")
                            valor_check = False

                #hasta aqui para comprobar el estado de los checkbox





                checkbox = ft.Checkbox(
                    scale=1.2,
                    value=valor_check,
                    disabled=check_deshabilitado,
                    on_change=lambda e, d=dia, t=i: on_checkbox_changed(e, d, t)
                )
                cells.append(
                    ft.DataCell(
                        ft.Container(
                            content=checkbox,
                            alignment=ft.alignment.center,
                        )
                    )
                )
                lista_estado_checkbox.append(valor_check)
            

            todos_checkbox=all(lista_estado_checkbox)
            valor_check_general=todos_checkbox              
            lista_estado_checkbox.clear()
            
            

            checkbox_general = ft.Checkbox(
                scale=1.2,
                value=valor_check_general,
                disabled=check_deshabilitado,
                on_change=lambda e, d=dia: on_checkbox_general_changed(e, d)
            )
            cells.append(
                ft.DataCell(
                    ft.Container(
                        content=checkbox_general,
                        alignment=ft.alignment.center,
                    )
                )
            )


            
            rows.append(ft.DataRow(cells=cells))

        # Crear la tabla pasando las columnas en la inicialización
        table = ft.DataTable(
            columns=columns,
            rows=rows,            
            bgcolor="#eed8cc",
            border=ft.border.all(2, ft.colors.WHITE),
            border_radius=8,            
            horizontal_lines=ft.border.BorderSide(2, ft.colors.WHITE),
            heading_row_height=50,
            data_row_min_height=50,
            data_row_max_height=50,
        )

        # Envolver la tabla en un ListView para permitir scroll si es necesario
        return ft.Container(
            content=ft.ListView(
                [table],
                expand=1,
                spacing=10,
                padding=20,
            ),
            
            border_radius=10,
            padding=20,
        )
    


    flecha_izquierda3 = ft.Container(
        content=ft.IconButton(
            icon=ft.icons.ARROW_CIRCLE_LEFT, 
            icon_size=40,                              
            on_click=mes_menos3,
            icon_color=ft.colors.BLUE_800 ,
            disabled= True
        )
    )  

    flecha_derecha3 = ft.Container(
        content=ft.IconButton(
            icon=ft.icons.ARROW_CIRCLE_RIGHT, 
            icon_size=40,
            on_click=mes_mas3,
            icon_color=ft.colors.BLUE_800 ,
            disabled= False
        )
    )

    fila_header3 = ft.Row(
        controls=[flecha_izquierda3, calendar_header3, flecha_derecha3],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=15
    )

    container_por_dias_semana=montar_calendario_por_dias_semana()

    columna_de_tab3=ft.Column(controls=[
            fila_header3, 
            container_por_dias_semana, 
            ft.Container(height=240),
            leyenda2,
            
            ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

     
    
    def on_tabs_changed(e):
        """
        Maneja cambios entre pestañas, actualizando la vista correspondiente.
        """
        index = e.control.selected_index
        if index == 0:
            mostrar_mes()
            actualizar_estado_botones()
            montar_calendario()
        elif index == 1:
            mostrar_mes2() 
            actualizar_estado_botones2()
            columna_de_tab2.controls[1] = montar_calendario_por_turno()
        elif index == 2:
            mostrar_mes3()
            actualizar_estado_botones3()
            columna_de_tab3.controls[1] = montar_calendario_por_dias_semana()
        elif index == 3:
            crear_tabla_tareas_usuarios()
        
        page.update()         


    # Configuración de pestañas principales
    tabs=ft.Tabs(
        selected_index=0,
        animation_duration=300,
        on_change=on_tabs_changed,
        tabs=[
            ft.Tab(text="Ver Tareas asignadas", icon=ft.icons.TASK, content=columna_tareas_asignadas),
            ft.Tab(text="Calendario por día", icon=ft.icons.CALENDAR_MONTH, content=columna_calendario_disponibilidad),
            ft.Tab(text="Calendario por turno", icon=ft.icons.CALENDAR_MONTH, content=columna_de_tab2),
            ft.Tab(text="Calendario por dia de semana", icon=ft.icons.CALENDAR_MONTH, content=columna_de_tab3),
            
        ],
        expand=1,

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
                    image_opacity=0.2,
                    margin=ft.margin.only(top=50)  # La imagen comenzará 50px más abajo
                ),
                ft.Container(
                    content=tabs,
                    expand=True,
                    bgcolor=ft.colors.TRANSPARENT,
                )
            ]
        ),
        expand=True
    )      
    
    return ft.View("/user", controls=[main_container])