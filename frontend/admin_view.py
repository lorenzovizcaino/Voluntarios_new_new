"""
Módulo principal de la vista de administración de tareas de voluntariado.
Implementa las funcionalidades para crear, editar, asignar y gestionar tareas,
incluyendo asignación automática y gestión de voluntarios.
"""

from datetime import datetime
import sys
import os
import flet as ft
import requests
import time
from openpyxl import Workbook
from calendar_widget import SpanishCalendar
from utils import (
    API_URL_TAREAS, guardar_notificacion, get_id_usuario_logeado, API_URL_LOGIN,
    API_URL_TAREAS_ASIGNADAS, API_URL_TAREAS_EDIT_COORDINADOR, API_URL_DATOS_USER,
    API_URL_TURNOS_DISPONIBLES, API_URL_USERS_ASIGNADOS, API_URL_LOGIN_DATOS,
    get_selected_tab_index, path_fondo, obtener_tarea_completa, obtener_nombre_usuario
)
from enviar_email import enviar_correo

class TareaSelecionada:
    """
    Clase para mantener el estado de una tarea seleccionada.
    Se usa para compartir información entre diferentes vistas.
    """
    def __init__(self):
        self.tarea_seleccionada = None

# Instancias globales para compartir estado entre vistas
tarea_para_asignar = TareaSelecionada()
tarea_para_editar = TareaSelecionada()




def admin(page: ft.Page):
    """
    Función principal que implementa la vista de administración.
    
    Args:
        page (ft.Page): Objeto page de Flet para la interfaz gráfica
        
    Returns:
        ft.View: Vista principal de administración
    """
    # Configuración inicial de la ventana
    page.window_width = 1050
    page.window_height = 900  
    page.window_center()
    page.bgcolor = ft.colors.TRANSPARENT
    page.window_bgcolor = ft.colors.TRANSPARENT    
    page.title="RedAyuda"
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER

    def salir(e):
        """Sale de la aplicacion"""        
        page.window_close()



    
    fecha_info = ft.Text(size=16)
    titulo=ft.Text(value="Tareas de Voluntariado", size=24, color=ft.colors.BLACK)


    usuario = ft.Text(value=obtener_nombre_usuario(), size=23, color=ft.colors.BLUE_800)
    icono_salir = ft.IconButton(icon=ft.icons.LOGOUT, icon_size=25, on_click=salir, icon_color=ft.colors.BLUE_800)
    fila_encabezado = ft.Row(
        controls=[
            ft.Container(titulo, expand=True),  # Expande el título a la izquierda
            ft.Row(
                controls=[usuario, icono_salir], 
                alignment=ft.MainAxisAlignment.END  # Alinea a la derecha
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,  # Mantiene el layout ordenado
        vertical_alignment=ft.CrossAxisAlignment.START  # Alinea arriba
    )
    


    # Variables de control
    year_seleccionado=None
    month_seleccionado=None
    day_seleccionado=None
    calendario_valido=False
    

    
    
    # Información de turnos
    leyenda2=ft.Text(value="Turno 1: de 09:00 a 12:00    Turno 2: de 12:00 a 15:00     Turno 3: de 15:00 a 18:00     Turno 4: de 18:00 a 21:00",
                        size=15,
                        weight=ft.FontWeight.BOLD)

    
    # Campos de entrada para crear tareas
    nombre_tarea = ft.Container(
        content=ft.TextField(
            label="Nombre de la tarea (mínimo 3 caracteres)",
            width=800,
            border_radius=0
        ),
        bgcolor=ft.colors.with_opacity(0.8, ft.colors.RED_50),
        
    
    )


    ubicacion_tarea = ft.Container(
        content=ft.TextField(
            label="Ubicacion de la tarea (mínimo 3 caracteres)",
            width=800,
            border_radius=0
        ),
        bgcolor=ft.colors.with_opacity(0.8, ft.colors.RED_50),
        
    
    )


    
    def on_date_selected(date_info):        
        """
        Maneja la selección de fecha en el calendario.
        
        Args:
            date_info (dict): Información de la fecha seleccionada
        """
        if date_info:
            nonlocal year_seleccionado, month_seleccionado, day_seleccionado
            year_seleccionado = date_info['year']
            month_seleccionado = date_info['month']
            day_seleccionado = date_info['day']            
            print(f"{day_seleccionado}/{month_seleccionado}/{year_seleccionado}")      
            page.update()

    

    def boton_deshabilitado():
        """
        Configura el estado deshabilitado del botón de guardar tarea.
        """
        boton_guardar_tarea.disabled=True
        boton_guardar_tarea.style= ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=5),
            bgcolor=ft.colors.GREY_400,
            color="BLACK",
            side=ft.BorderSide(width=1, color=ft.colors.BLACK))
        
        
    def boton_habilitado():
        """
        Configura el estado habilitado del botón de guardar tarea.
        """
        boton_guardar_tarea.disabled=False
        boton_guardar_tarea.style= ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=5),
            bgcolor=ft.colors.GREEN_200,
            color="BLACK",
            side=ft.BorderSide(width=1, color=ft.colors.BLACK))
        

    

    def estado_boton_guardar_tarea():      
        """
        Verifica y actualiza el estado del botón de guardar tarea
        según la validez de los campos requeridos.
        """        
        nonlocal calendario_valido
        nombre_valido = bool(nombre_tarea.content.value and nombre_tarea.content.value.strip())
        ubicacion_valida = bool(ubicacion_tarea.content.value and ubicacion_tarea.content.value.strip())
        turnos_valido = bool(lista_turnos.value)
        voluntarios_valido = bool(voluntarios_necesarios.value)                
        
       
        if all([nombre_valido, ubicacion_valida, turnos_valido, voluntarios_valido, calendario_valido]):
            boton_habilitado()            
        else:
            boton_deshabilitado()            
        page.update()    

    # Manejadores de eventos para los campos de entrada
    def on_evento_nombre_tarea(e):        
        estado_boton_guardar_tarea()

    def on_evento_ubicacion_tarea(e):
        estado_boton_guardar_tarea()

    def on_evento_lista_turnos(e):        
        estado_boton_guardar_tarea()

    def on_evento_voluntarios_necesarios(e):        
        estado_boton_guardar_tarea()

    def on_evento_calendario(e):     
        nonlocal calendario_valido 
        calendario_valido=True  
        estado_boton_guardar_tarea()

    def guardar_tarea(e):
        """
        Guarda una nueva tarea en el sistema.
        
        Args:
            e: Evento de Flet
        
        Efectos:
            - Crea una nueva tarea en la base de datos
            - Actualiza la interfaz
            - Muestra notificación de resultado
        """
        nonlocal calendario_valido
        mensaje_boton_guardar = ""      
        
        data = {
            "user_id": get_id_usuario_logeado(), 
            "tarea_name": nombre_tarea.content.value,
            "tarea_ubicacion": ubicacion_tarea.content.value,
            "year": year_seleccionado, 
            "month": month_seleccionado, 
            "day": day_seleccionado, 
            "turno": lista_turnos.value, 
            "voluntarios_necesarios": voluntarios_necesarios.value,     
            "coordinador":check_coordinador.value
        }
        
        response = requests.post(API_URL_TAREAS, json=data)
        if response.status_code == 201:
            mensaje_boton_guardar = f"Tarea {nombre_tarea.content.value} guardada correctamente"
            crear_lista_tabla()
        else:
            mensaje_boton_guardar = "Error al guardar, la tarea necesita un minimo de 3 caracteres"
        
        # Mostrar notificación
        snack_bar = ft.SnackBar(content=ft.Text(mensaje_boton_guardar))
        page.overlay.append(snack_bar)
        snack_bar.open = True
        
        # Limpiar campos
        nombre_tarea.content.value = ""
        ubicacion_tarea.content.value = ""
        lista_turnos.value = None
        voluntarios_necesarios.value = None    
        boton_deshabilitado()
        calendar.reset_calendar()
        calendario_valido=False 
        check_coordinador.value=False
        page.update()


    # Crear instancia del calendario
    calendar = SpanishCalendar(on_date_selected)
    check_coordinador=ft.Checkbox(label="Necesita Coordinador", value=False)

    lista_turnos = ft.Dropdown(
        width=250,
        height=40,
        options=[
            ft.dropdown.Option("Turno 1"),
            ft.dropdown.Option("Turno 2"),
            ft.dropdown.Option("Turno 3"),
            ft.dropdown.Option("Turno 4"),
        ],
        hint_text="     Selección de Turno",
        hint_style=ft.TextStyle(
            size=14,
            color=ft.colors.BLACK,
        ),
        bgcolor="#e3f2fd",
        border_color=ft.colors.BLACK,
        text_size=15,
        value=None  # Asegurarse de que empiece en None
    )

    voluntarios_necesarios = ft.Dropdown(
        width=250,
        height=40,
        options=[
            ft.dropdown.Option("1"),
            ft.dropdown.Option("2"),
            ft.dropdown.Option("3"),
            ft.dropdown.Option("4"),
            ft.dropdown.Option("5"),
        ],
        hint_text="     Voluntarios necesarios",
        hint_style=ft.TextStyle(
            size=14,
            color=ft.colors.BLACK,
            
        ),
        bgcolor="#e3f2fd",
        border_color=ft.colors.BLACK,
        text_size=15,
        value=None  # Asegurarse de que empiece en None
    )

 

    boton_guardar_tarea=ft.ElevatedButton(text="Guardar Tarea",
                            width=250,
                            height=40,
                            icon=ft.icons.SAVE,
                            on_click=guardar_tarea,
                            disabled=True,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=5), 
                                bgcolor=ft.colors.GREY_400,
                                color="BLACK",
                                side=ft.BorderSide(width=1, color=ft.colors.BLACK), #borde del boton

                                ),
                            )
    
    # Organización de elementos en contenedores
    conte=ft.Container(height=20)
    contenedor=ft.Container(ft.Column(controls=[check_coordinador, lista_turnos, voluntarios_necesarios, boton_guardar_tarea],spacing=30), padding=30)
    

     
    fila = ft.Container(
        content=ft.Row(
            controls=[
                calendar,
                contenedor
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        bgcolor=ft.colors.with_opacity(0.8, ft.colors.RED_50),
        width=800,        
        border=ft.border.all(width=1, color=ft.colors.BLACK)
)
    
    contenedor = ft.Container(
        content=ft.Column(
            controls=[
                      conte,
                      nombre_tarea, 
                      ubicacion_tarea, 
                      fila,
                      ft.Container(height=80),
                      leyenda2],
            spacing=20,
            ),
        padding=ft.padding.only (left=100),
        
        
        )

    # Asignación de manejadores de eventos
    nombre_tarea.on_change = on_evento_nombre_tarea
    ubicacion_tarea.on_change = on_evento_ubicacion_tarea
    lista_turnos.on_change = on_evento_lista_turnos
    voluntarios_necesarios.on_change = on_evento_voluntarios_necesarios
    calendar.on_change=on_evento_calendario
    
    
    crear_tareas = ft.Column(controls=[contenedor])







    #Contenido para la pestaña de Asignar Tareas
    lista_para_tabla=[]

    def cargar_datos():
        """
        Carga las tareas existentes desde la base de datos.
        
        Returns:
            dict: Datos de las tareas o None si hay error
        """
        
        try:
            response=requests.get(API_URL_TAREAS)
            if response.status_code==200:
                tareas_dict=response.json()
                return tareas_dict
            else:
                print(f"Error al obtener datos: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error en la conexión: {str(e)}")
            return None
        
    def borrar_registro(e, id):     
        """
        Elimina una tarea y gestiona las notificaciones asociadas.
        
        Args:
            e: Evento de Flet
            id (int): ID de la tarea a eliminar
        """  
        tarea_selecionada_completa=obtener_tarea_completa(id)
        for registro in lista_para_tabla:
            if registro["id"] == id:
                
                lista_para_tabla.remove(registro)  
                response=requests.get(f"{API_URL_USERS_ASIGNADOS}/{id}")
                requests.delete(f"{API_URL_TAREAS}/{id}")                   
                requests.delete(f"{API_URL_TAREAS_ASIGNADAS}/{id}") 
                #recuperamos los id de los usuarios que estaban asignados a la tarea borrada, si los hubiese 
                data=response.json()
                user_id_tarea_borrada=[]
                for user in data["users"]:
                    id_user=user["user_id"]
                    user_id_tarea_borrada.append(id_user)
                #una vez obtenidos los usuarios se envia correo y notificacion de cancelacion de la tarea
                for user in user_id_tarea_borrada:

                    asunto=f"Cancelada la tarea de voluntariado asignada el dia {tarea_selecionada_completa["day"]}/{tarea_selecionada_completa["month"]}/{tarea_selecionada_completa["year"]}"
                    mensaje=f"""
                            Estimado voluntario:
                            Se ha cancelado o modificado la tarea:
                            TAREA: {tarea_selecionada_completa["tarea_name"]}
                            UBICACION: {tarea_selecionada_completa["tarea_ubicacion"]}
                            DIA: {tarea_selecionada_completa["day"]}/{tarea_selecionada_completa["month"]}/{tarea_selecionada_completa["year"]}

                            Muchas gracias por su colaboracion
                            """

                    enviar_correo("antoniosantaballa@gmail.com",asunto, mensaje)

                    # Guardar notificación en el sistema
                    notification_data = {
                            "tarea_name": tarea_selecionada_completa["tarea_name"],
                            "tarea_ubicacion": tarea_selecionada_completa["tarea_ubicacion"],
                            "day": tarea_selecionada_completa["day"],
                            "month": tarea_selecionada_completa["month"],
                            "year": tarea_selecionada_completa["year"],
                            "turno": tarea_selecionada_completa["turno"]
                        }
                        
                    # Guardar la notificación para mostrarla cuando el usuario haga login
                    guardar_notificacion(user, notification_data, alta_baja_tarea=False)
                                                   
                break  
        cuadro_dialogo.open = False     
        actualizar_tabla()

    def asignar_tarea(e, dato):      
        """
        Prepara la asignación de una tarea y navega a la vista de asignación.
        
        Args:
            e: Evento de Flet
            dato (dict): Datos de la tarea a asignar
        """  
        tarea_para_asignar.tarea_seleccionada=dato              
        page.go("/admin/assign")

    def editar_tarea(e, tarea):
        """
        Prepara la edición de una tarea y navega a la vista de edición.
        
        Args:
            e: Evento de Flet (no utilizado)
            tarea (dict): Datos de la tarea a editar
        """
        tarea_para_editar.tarea_seleccionada=tarea            
        page.go("/admin/edit")

    def crear_lista_tabla():    
        """
        Crea la lista de tareas para mostrar en la tabla.
        Actualiza la visualización de la tabla.
        """
        dicionario_base_datos=cargar_datos()
        lista_para_tabla.clear()
        for tarea in dicionario_base_datos:
            
            id=tarea["id"]
            nombre=tarea["tarea_name"]
            ubicacion=tarea["tarea_ubicacion"]
            fecha=f"{tarea["day"]}/{tarea["month"]}/{tarea["year"]}"
            turno=tarea["turno"]
            v_necesarios=tarea["voluntarios_necesarios"]
            v_asignados=tarea["voluntarios_asignados"]
            coordinador=tarea["coordinador"]
            lista_para_tabla.append({"id":id,"nombre":nombre, "ubicacion": ubicacion, "fecha":fecha,"turno":turno,"voluntarios_necesarios":v_necesarios,"voluntarios_asignados":v_asignados, "coordinador":coordinador})
        actualizar_tabla()


    
        

    
 



    



    def guardar_excel(e):
        """
        Exporta los datos de la tabla a un archivo Excel.
        
        Args:
            e: Evento de Flet
        """
        wb = Workbook()
        ws = wb.active
        ws.title = "Tareas Voluntariado"
        ws.append(["Tareas", "Ubicacion", "Fecha", "Turno", "Voluntarios necesarios", "Voluntarios asignados", "Coordinador"])
        
        for row in data_table.rows:
            valores_fila = []
            for cell in row.cells[:7]:  # Limitamos a 7 columnas (excluyendo Acciones)
                               
                # Si el contenido es un Container, intentamos obtener su contenido interno
                if hasattr(cell.content, 'content'):
                    contenido_interno = cell.content.content
                    # Si el contenido interno tiene un valor, lo usamos
                    if hasattr(contenido_interno, 'value'):
                        valor_celda = contenido_interno.value
                    else:
                        valor_celda = str(contenido_interno)
                # Si no es un Container, intentamos obtener el valor directamente
                elif hasattr(cell.content, 'value'):
                    valor_celda = cell.content.value
                else:
                    valor_celda = str(cell.content)
                    
                valores_fila.append(valor_celda)
                

            if any(valores_fila):
                ws.append(valores_fila)

        # Ajustar el ancho de las columnas
        for column in ws.columns:
            max_length = 0
            column = list(column)
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = (max_length + 2)
            ws.column_dimensions[column[0].column_letter].width = adjusted_width

        fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"{fecha_hora}_Tareas voluntariado.xlsx"
        wb.save(nombre_archivo)
        snack_bar = ft.SnackBar(content=ft.Text(f"Datos guardados en {nombre_archivo}"))
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()
        
    def actualizar_tabla():
        """
        Actualiza la visualización de la tabla de tareas.
        Aplica formatos y colores según el estado de las tareas.
        """
        data_table.rows.clear()

        for dato in lista_para_tabla:
            
            if dato["voluntarios_necesarios"]==dato["voluntarios_asignados"]:
                color=ft.colors.GREEN
            else:
                color=ft.colors.BLACK
            data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(dato["nombre"], size=14, color=color), 
                                padding=ft.padding.all(5),
                                alignment=ft.alignment.center_left
                                
                                
                            )
                        ),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(dato["ubicacion"], size=14, color=color), 
                                padding=ft.padding.all(5),
                                alignment=ft.alignment.center_left
                                
                                
                            )
                        ),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(dato["fecha"], size=14, color=color),
                                padding=ft.padding.all(5),
                                alignment=ft.alignment.center
                            )
                        ),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(dato["turno"], size=14, color=color),
                                padding=ft.padding.all(5),
                                alignment=ft.alignment.center
                            )
                        ),
                        ft.DataCell(
                            
                            ft.Container(
                                content=ft.Text(str(dato["voluntarios_necesarios"]), size=14, color=color),
                                padding=ft.padding.all(5),
                                alignment=ft.alignment.center
                            )
                        ),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(str(dato["voluntarios_asignados"]), size=14, color=color),
                                padding=ft.padding.all(5),
                                alignment=ft.alignment.center
                            )
                        ),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Checkbox(value=dato["coordinador"], disabled=True),
                                padding=ft.padding.all(5),
                                alignment=ft.alignment.center
                            )
                        ),
                        ft.DataCell(
                            ft.Row(
                                
                                controls=[
                                    ft.IconButton(
                                        ft.icons.DELETE_OUTLINE,
                                        tooltip="Borrar",
                                        icon_color="red",
                                        on_click=lambda e, id=dato["id"]: show_dialog(e, id)
                                    ),
                                    ft.IconButton(
                                        ft.icons.SEARCH,
                                        tooltip="Asignar voluntarios",
                                        icon_color="Green",
                                        on_click=lambda e, dato=dato: asignar_tarea(e, dato)
                                    ),
                                    ft.IconButton(
                                        ft.icons.EDIT_OUTLINED,
                                        tooltip="Editar",
                                        icon_color="Blue",
                                        on_click=lambda e, dato=dato: editar_tarea(e, dato)
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=0
                                
                                
                            )
                        ),
                    ]
                )
            )
        page.update()

    
    def show_dialog(e, id):
        """
        Muestra el diálogo de confirmación para borrar una tarea.
        En show_dialog, en lugar de solo establecer open = True, primero actualizamos el manejador de eventos (on_click) del botón Aceptar con una nueva función lambda que tiene el ID correcto.
        actions[0] se refiere al primer botón en el array de actions del AlertDialog (el botón "Aceptar").
        
        Args:
            e: Evento de Flet (no utilizado)
            id (int): ID de la tarea a borrar
        """
        
        
        cuadro_dialogo.actions[0].on_click = lambda e, id=id: borrar_registro(e, id)
        cuadro_dialogo.open = True
        page.update()

    def close_dialog(e):
        """Cierra el diálogo de confirmación."""
        cuadro_dialogo.open = False
        page.update()

    def cancelar_clicked(e):   
        """Maneja el evento de cancelar en el diálogo."""     
        close_dialog(e)
        page.update()


    def obtener_id_voluntarios_disponibles2(tarea_completa):
        """
        Obtiene los IDs de voluntarios disponibles para una tarea específica.
        
        Args:
            tarea_completa (dict): Información completa de la tarea
            
        Returns:
            list: Lista de IDs de voluntarios disponibles, None si hay error
        """
        usuarios = []
        usuariosfinales = []
        id_tareas_usuario = []
        
        data = {
            "year": tarea_completa["year"],
            "month": tarea_completa["month"],
            "day": tarea_completa["day"],
            "turno": tarea_completa["turno"]
        }

        # Obtener usuarios disponibles
        try:
            response = requests.get(API_URL_TURNOS_DISPONIBLES, params=data)
            if response.status_code==200:
                
                usuarios_disponibles=response.json()
                for user in usuarios_disponibles:
                    response2=requests.get(f"{API_URL_TAREAS}/{tarea_completa['id']}")
                    tarea_consulta=response2.json()
                    
                    coordinador_ingresado=tarea_consulta["coordinador_Asignado"]
                    
                    if tarea_completa["coordinador"]: #and  coordinador_ingresado==False:                    
                        usuarios.append(user["user_id"])
                        #poner a True que el coordinador esta elegido si el usuario es coordinador
                        #FALTA QUE EL COORDINADOR ELEGIDO SEA EL DE MENOS TAREAS, DE MOMENTO AÑADE EL PRIMERO POR id
                        #requests.put(f"{API_URL_TAREAS_EDIT_COORDINADOR}/{tarea_completa["id"]}",params={"coordinador_Asignado": True})
                        
                        
                    else:                                      
                        response2=requests.get(f"{API_URL_DATOS_USER}/{user['user_id']}")                
                        user_data2=response2.json()
                        if user_data2["coordinador"]==False:
                            usuarios.append(user["user_id"])

            # if response.status_code == 200:
            #     usuarios_disponibles = response.json()

            #     for user in usuarios_disponibles:
            #         usuarios.append(user["user_id"])
                
            else:
                print(f"Error al obtener datos1: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error en la conexión1: {str(e)}")
            return None
        
        usuariosfinales = usuarios.copy()
        fecha_tarea = f"{tarea_completa['day']}/{tarea_completa['month']}/{tarea_completa['year']}"

        # Comprobar tareas existentes de usuarios
        for user in usuarios:
            try:
                response = requests.get(f"{API_URL_TAREAS_ASIGNADAS}/{user}")
                if response.status_code == 200:
                    data = response.json()
                    tareas_usuario = data["tareas"]
                    
                    # Verificar cada tarea del usuario
                    for tarea in tareas_usuario:
                        tarea_response = requests.get(f"{API_URL_TAREAS}/{tarea['tarea_id']}")
                        if tarea_response.status_code == 200:
                            tarea_data = tarea_response.json()
                            fecha_existente = f"{tarea_data['day']}/{tarea_data['month']}/{tarea_data['year']}"
                            
                            if fecha_existente == fecha_tarea:
                                if user in usuariosfinales:
                                    usuariosfinales.remove(user)
                                break
                else:
                    print(f"Error al obtener datos2: {response.status_code}")
                    continue
            except Exception as e:
                print(f"Error en la conexión2: {str(e)}")
                continue

        if len(usuariosfinales) == 0:
            print("No hay voluntarios disponibles para esta tarea")
        return usuariosfinales
    
    def asignar_tarea_autoasignar(tarea_completa, id_voluntario):
        """
        Asigna automáticamente una tarea a un voluntario.
        
        Args:
            tarea_completa (dict): Información completa de la tarea
            id_voluntario (int): ID del voluntario a asignar
        """      

        data_tarea = {
                "id": tarea_completa["id"],
                "user_id": tarea_completa["id"],  
                "tarea_name": tarea_completa["tarea_name"],  
                "tarea_ubicacion": tarea_completa["tarea_ubicacion"],  
                "year": tarea_completa["year"],
                "month": tarea_completa["month"],
                "day": tarea_completa["day"],
                "turno": tarea_completa["turno"],
                "voluntarios_necesarios": tarea_completa["voluntarios_necesarios"],
                "coordinador": tarea_completa["coordinador"]
            }


        params_tarea={
            "id":tarea_completa["id"],
            "id_voluntario":id_voluntario
        }

        data_tarea_asignada={
            "tarea_id":tarea_completa["id"],
            "user_id":id_voluntario

        }
        
        # Actualizar asignaciones
        response=requests.put(f"{API_URL_TAREAS}/{tarea_completa['id']}",json=data_tarea, params=params_tarea)
        response2=requests.post(API_URL_TAREAS_ASIGNADAS, json=data_tarea_asignada)
        
        # Enviar notificaciones
        asunto=f"Nueva tarea de voluntariado asignada el dia {tarea_completa["day"]}/{tarea_completa["month"]}/{tarea_completa["year"]}"
        mensaje=f"""
                Estimado voluntario:
                Se le ha asignado una nueva tarea:
                TAREA: {tarea_completa["tarea_name"]}
                UBICACION: {tarea_completa["tarea_ubicacion"]}
                DIA: {tarea_completa["day"]}/{tarea_completa["month"]}/{tarea_completa["year"]}

                Muchas gracias por su colaboracion
                """

        enviar_correo("antoniosantaballa@gmail.com",asunto, mensaje)

        # Guardar notificación para mostrarla cuando el usuario haga login
        notification_data = {
                "tarea_name": tarea_completa["tarea_name"],
                "tarea_ubicacion": tarea_completa["tarea_ubicacion"],
                "day": tarea_completa["day"],
                "month": tarea_completa["month"],
                "year": tarea_completa["year"],
                "turno": tarea_completa["turno"]
            }
            
        
        guardar_notificacion(id_voluntario, notification_data, alta_baja_tarea=True)
        

        
    
    def obtener_amigo(id_usuario):
        """
        Obtiene el amigo asignado a un usuario.
        
        Args:
            id_usuario (int): ID del usuario
            
        Returns:
            str: Nombre del amigo o "no tiene amigo asignado"
        """
        response_datos_usuario=requests.get(f"{API_URL_DATOS_USER}/{id_usuario}")
        data_amigo=response_datos_usuario.json()
        amigo=data_amigo["amigo"] or "no tiene amigo asignado"
        return amigo
    
    def comprobar_amigo(id_usuario):
        """
        Verifica si existe una relación de amistad recíproca.
        
        Args:
            id_usuario (int): ID del usuario a verificar
            
        Returns:
            int: ID del amigo si la relación es recíproca, None en caso contrario
        """

        #obtenemos username del usuario
        response_datos_usuario=requests.get(f"{API_URL_LOGIN}/{id_usuario}")
        data_usuario=response_datos_usuario.json()
        username_usuario=data_usuario["username"]
        
        #obtener el amigo del id_usuario
        amigo=obtener_amigo(id_usuario)
        
        if amigo=="no tiene amigo asignado":
            return None
        else:
            #comprobar que la amistad sea reciproca

            #obtenemos la id del amigo
            response_id_amigo=requests.get(f"{API_URL_LOGIN_DATOS}/{amigo}")
            data_response_id_amigo=response_id_amigo.json()
            print(f"data_response_id_amigo: {data_response_id_amigo}")
            id_amigo=data_response_id_amigo["id"]
            #con la id_amigo vemos si la amistad es reciproca con id_usuario
            amigo_del_amigo=obtener_amigo(id_amigo)

        # Retornar id_amigo solo si la amistad es recíproca    
        if amigo_del_amigo==username_usuario:
            return id_amigo
        else:
            return None
    

            
        

        



    def auto_asignar_tareas(e):
        """
        Realiza la asignación automática de tareas a voluntarios.
        Considera amistades recíprocas y coordinadores necesarios.
        
        Args:
            e: Evento de Flet
        """
        # Configurar barra de progreso
        barra_progreso = ft.ProgressBar(width=800, color="green", bgcolor="#eeeeee")
        texto_barra_progreso = ft.Text("Iniciando asignación de tareas...", size=16)
        
        # Crear el contenedor de progreso
        progress_container = ft.Container(
            content=ft.Column([
                barra_progreso,
                texto_barra_progreso
            ], 
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            bgcolor=ft.colors.with_opacity(0.9, ft.colors.WHITE),
            border_radius=10,
            border=ft.border.all(1, ft.colors.GREY_400),
            width=900,
            height=100,
        )
        
        # Crear un contenedor oscuro semitransparente que cubra toda la pantalla
        overlay = ft.Container(
            bgcolor=ft.colors.with_opacity(0.5, ft.colors.BLACK),
            expand=True
        )
        
        # Crear un Stack que centre el contenedor de progreso
        stack_container = ft.Stack(
            controls=[
                overlay,
                ft.Container(
                    content=progress_container,
                    alignment=ft.alignment.center,
                    expand=True
                )
            ],
            expand=True
        )
        
        # Añadir el stack a la página
        page.overlay.append(stack_container)
        page.update()
        
        # calcular el total de tareas que se necesita asignar
        total_tareas_para_asignar = 0
        for lista in lista_para_tabla:
            voluntarios_necesarios = lista["voluntarios_necesarios"]
            voluntarios_asignados = lista["voluntarios_asignados"] or 0
            if voluntarios_necesarios > voluntarios_asignados:
                total_tareas_para_asignar += 1
                
        if total_tareas_para_asignar == 0:
            texto_barra_progreso.value = "No hay tareas pendientes de asignar"
            page.update()
            time.sleep(2)
            page.overlay.remove(stack_container)
            page.update()
            return
        
        tarea_actual = 0
        
        # Procesar cada tarea
        for lista in lista_para_tabla:
            lista_usuarios_tareas = []
            lista_coordinadores_tareas = []
            id_voluntarios_rasos=[]
            id_voluntarios_coordinadores=[]
            id_amigo=None
            
            voluntarios_necesarios = lista["voluntarios_necesarios"]
            voluntarios_assignados = lista["voluntarios_asignados"] or 0
            
            #este if comprueba que la tarea aun no esta completa con todos los usuarios    
            if voluntarios_necesarios > voluntarios_assignados:
                tarea_actual += 1
                barra_progreso.value = tarea_actual / total_tareas_para_asignar
                texto_barra_progreso.value = f"Procesando tarea: {lista['nombre']} ({tarea_actual}/{total_tareas_para_asignar})"
                page.update()
                
                tarea_completa = obtener_tarea_completa(lista["id"])
                id_voluntarios_disponibles = obtener_id_voluntarios_disponibles2(tarea_completa)
                

                if id_voluntarios_disponibles is None:
                    continue





                # Separar voluntarios por rol
                for id_voluntario in id_voluntarios_disponibles:
                    response2=requests.get(f"{API_URL_DATOS_USER}/{id_voluntario}")                
                    user_data2=response2.json()
                    if user_data2["coordinador"]:
                        id_voluntarios_coordinadores.append(id_voluntario)
                    else:
                        id_voluntarios_rasos.append(id_voluntario)

               

                
                # Verificar estado del coordinador
                response2=requests.get(f"{API_URL_TAREAS}/{tarea_completa['id']}")
                tarea_consulta=response2.json()                    
                coordinador_ingresado=tarea_consulta["coordinador_Asignado"]

                #si se cumple el siguiente if es que es necesario un coordinador
                if len(id_voluntarios_coordinadores)>0 and not coordinador_ingresado:
                    for voluntario_coordinador in id_voluntarios_coordinadores:
                        response_contar = requests.get(f"{API_URL_TAREAS_ASIGNADAS}/{voluntario_coordinador}/count")
                        numero_tareas = response_contar.json()
                        lista_coordinadores_tareas.append(numero_tareas)

                    lista_coordinadores_tareas.sort(key=lambda x: x['total_tareas'], reverse=False)
                    asignar_tarea_autoasignar(tarea_completa, lista_coordinadores_tareas[0]['user_id'])
                    
                    id_amigo=comprobar_amigo(lista_coordinadores_tareas[0]['user_id'])
                    
                    



                    requests.put(f"{API_URL_TAREAS_EDIT_COORDINADOR}/{tarea_completa["id"]}",params={"coordinador_Asignado": True})

                    # voluntarios_assignados si se asigna un coordinador ya cuenta como voluntario
                    voluntarios_assignados+=1     


                
                # Asignar voluntarios rasos 
                voluntarios_restantes = voluntarios_necesarios - voluntarios_assignados
                if voluntarios_restantes >= len(id_voluntarios_rasos):
                    for voluntario in id_voluntarios_rasos:
                        asignar_tarea_autoasignar(tarea_completa, voluntario)
                        texto_barra_progreso.value = f"Asignando voluntario a la tarea: {lista['nombre']}"
                        page.update()
                else:

                    #bucle para añadir amigos antes que por acumumacion tareas
                    while True or voluntarios_restantes !=0:
                        
                        if id_amigo in id_voluntarios_rasos:
                            asignar_tarea_autoasignar(tarea_completa, id_amigo)
                            copia_id_amigo=id_amigo
                            id_voluntarios_rasos.remove(id_amigo)#quitar de la lista
                            id_amigo=comprobar_amigo(copia_id_amigo)
                            voluntarios_assignados+=1
                            voluntarios_restantes = voluntarios_necesarios - voluntarios_assignados
                        else:
                            break


                    # Asignar voluntarios por número de tareas acumuladas                    
                    for voluntario in id_voluntarios_rasos:
                        
                        response_contar = requests.get(f"{API_URL_TAREAS_ASIGNADAS}/{voluntario}/count")
                        numero_tareas = response_contar.json()
                        lista_usuarios_tareas.append(numero_tareas)
                    
                    lista_usuarios_tareas.sort(key=lambda x: x['total_tareas'], reverse=False)
                    
                    for i in range(0, voluntarios_restantes):
                        asignar_tarea_autoasignar(tarea_completa, lista_usuarios_tareas[i]['user_id'])
                        texto_barra_progreso.value = f"Asignando voluntario {i+1}/{voluntarios_restantes} a la tarea: {lista['nombre']}"
                        page.update()
        
        # Finalizar asignación
        barra_progreso.value = 1
        texto_barra_progreso.value = "¡Asignación de tareas completada!"
        page.update()
        
        
        time.sleep(2)
        page.overlay.remove(stack_container)
        page.update()
        
        
        crear_lista_tabla()



    



    # Configuración de componentes de la interfaz
    titulo_asignar_tareas=ft.Text(value="Listado de Tareas:", size=18, color=ft.colors.BLACK)
    
    

    excel_icon = ft.IconButton(
        icon=ft.icons.TABLE_VIEW,  
        icon_color="#217346",      
        icon_size=40,            
        on_click=guardar_excel,
        tooltip="Guardar como Excel"
    )

    row_cabecera=ft.Row(controls=[titulo_asignar_tareas, excel_icon],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,)

    
    # Configuración de la tabla de datos
    data_table = ft.DataTable(
    
        bgcolor=ft.colors.with_opacity(0.8, ft.colors.RED_50),      
        #border=ft.border.all(width=1, color=ft.colors.BLUE_GREY_100),
        border_radius=8,        
        
        vertical_lines=ft.border.BorderSide(1, ft.colors.BLUE_GREY_50),
        horizontal_lines=ft.border.BorderSide(1, ft.colors.BLUE_GREY_50),
        
        
        columns=[            
            ft.DataColumn(
                label=ft.Container(
                    content=ft.Text(
                        "Tarea",
                        color=ft.colors.BLUE_GREY_800,
                        size=13,
                        weight=ft.FontWeight.W_500,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    width=155
                ),
                numeric=False,
            ),
            ft.DataColumn(
                label=ft.Container(
                    content=ft.Text(
                        "Ubicación",
                        color=ft.colors.BLUE_GREY_800,
                        size=13,
                        weight=ft.FontWeight.W_500,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    width=155
                ),
                numeric=False,
            ),

            ft.DataColumn(
                label=ft.Container(
                    content=ft.Text(
                        "Fecha",
                        color=ft.colors.BLUE_GREY_800,
                        size=13,
                        weight=ft.FontWeight.W_500,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    width=50
                ),
                numeric=False,
            ),
            ft.DataColumn(
                label=ft.Container(
                    content=ft.Text(
                        "Turno",
                        color=ft.colors.BLUE_GREY_800,
                        size=13,
                        weight=ft.FontWeight.W_500,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    width=70
                    
                ),
                numeric=False,
            ),
            ft.DataColumn(
                label=ft.Container(
                    content=ft.Text(
                        "Voluntarios necesarios",
                        color=ft.colors.BLUE_GREY_800,
                        size=13,
                        weight=ft.FontWeight.W_500,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    width=70
                    
                ),
                numeric=True,
            ),
            ft.DataColumn(
                label=ft.Container(
                    content=ft.Text(
                        "Voluntarios asignados",
                        color=ft.colors.BLUE_GREY_800,
                        size=13,
                        weight=ft.FontWeight.W_500,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    width=70
                ),
                numeric=True,
            ),
            ft.DataColumn(
                label=ft.Container(
                    content=ft.Text(
                        "Coordinador",
                        color=ft.colors.BLUE_GREY_800,
                        size=13,
                        weight=ft.FontWeight.W_500,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    width=80
                ),
                numeric=True,
            ),
            ft.DataColumn(
                label=ft.Container(
                    content=ft.Text(
                        "Acciones",
                        color=ft.colors.BLUE_GREY_800,
                        size=13,
                        weight=ft.FontWeight.W_500,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    alignment=ft.alignment.center,
                    width=100
                ),
                numeric=False,
            ),     
        ],
        
        
        heading_row_height=50,
        data_row_min_height=45,
        data_row_max_height=60,
        column_spacing=20,
        border=ft.border.all(color=ft.colors.BLUE_GREY_800, width=1),
        rows=[]
    )


    tabla_con_scroll = ft.ListView(
        controls=[data_table],
        expand=1,
        height=480, 
    )

    contenedor_tabla = ft.Container(
        content=tabla_con_scroll,
        width=1000,      
        
        padding=0,
    )    

    cuadro_dialogo = ft.AlertDialog(
        title=ft.Text("Borrar tarea"),
        content=ft.Text("¿Estás seguro de borrar la tarea?"),
        actions=[
            ft.TextButton("Aceptar", on_click=lambda e: None),  # Handler vacío inicial ya que  el handler real se asignará dinámicamente en show_dialog 
            ft.TextButton("Cancelar", on_click=cancelar_clicked),
        ],
    )

    # Configuración del botón de auto-asignación
    boton_auto_asignar_tareas=ft.ElevatedButton(text="Auto asignar Tareas",
                            width=300,
                            height=50,
                            icon=ft.icons.FLASH_AUTO,
                            on_click=auto_asignar_tareas,                            
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=5), 
                                bgcolor=ft.colors.GREEN_200,
                                color="BLACK",
                                side=ft.BorderSide(width=1, color=ft.colors.BLACK), 
                                text_style=ft.TextStyle(size=20)
                                ),
                            )
    
    contenedor_boton=ft.Container(content=boton_auto_asignar_tareas,
                                  alignment=ft.alignment.center_right)
    

    # Organización final de la interfaz
    contenido_asignar_tareas = ft.Container(
        content=ft.Column(
            controls=[row_cabecera, contenedor_tabla, cuadro_dialogo, contenedor_boton],
            spacing=20,
        ),
        #padding=ft.padding.only(top=20)
        padding=20
        )
    
    


    crear_lista_tabla()
    #fin pestaña asignar tareas


    


    # Configuración de pestañas
    tabs=ft.Tabs(
        selected_index=get_selected_tab_index(),
        animation_duration=300,
        
        tabs=[
            ft.Tab(text="Crear Tareas", icon=ft.icons.LIST_ALT, content=crear_tareas),
            ft.Tab(text="Asignar Tareas", icon=ft.icons.ASSIGNMENT_IND_SHARP, content=contenido_asignar_tareas),
           
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


    return ft.View("/admin", controls=[fila_encabezado,main_container])
