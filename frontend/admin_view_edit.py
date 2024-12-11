import flet as ft
import requests

from admin_view import tarea_para_editar
from utils import API_URL_TAREAS, API_URL_TAREAS_BORRAR, API_URL_DATOS_USER, API_URL_TAREAS_EDIT_COORDINADOR,get_id_usuario_logeado, API_URL_TURNOS_DISPONIBLES, API_URL_LOGIN, API_URL_TAREAS_ASIGNADAS, API_URL_TAREAS_EDIT, set_selected_tab_index,path_fondo
from enviar_email import enviar_correo
from calendar_widget import SpanishCalendar



def admin_edit(page: ft.Page):
    page.window_width = 1050
    page.window_height = 900  
    page.window_center()
    
    page.title="Tareas de Voluntariado"
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
    tarea_selecionada_completa=None

    year_seleccionado=None
    month_seleccionado=None
    day_seleccionado=None
    calendario_cambiado=False
    id_voluntarios_asignados=[]
    voluntarios_asignados=[]

    indicador_carga = ft.ProgressRing(width=100, height=100, stroke_width=8)
    overlay_carga = ft.Container(
            content=indicador_carga,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.with_opacity(0.7, ft.colors.WHITE),
            visible=False,
            expand=True
        )

    def obtener_tarea_completa():
        
        try: 

            response=requests.get(f"{API_URL_TAREAS}/{tarea_para_editar.tarea_seleccionada["id"]}")
            if response.status_code==200:
                tarea_completa=response.json()
                return tarea_completa
            else:
                print(f"Error al obtener datos: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error en la conexión: {str(e)}")
            return None
        

    tarea_selecionada_completa=obtener_tarea_completa()
    
    





    def montar_contenido_edit():

        



        def on_date_selected(date_info):              
            nonlocal year_seleccionado, month_seleccionado, day_seleccionado,calendario_cambiado
            calendario_cambiado=True   
            if date_info:                
                year_seleccionado = date_info['year']
                month_seleccionado = date_info['month']
                day_seleccionado = date_info['day']
                page.update()


        def guardar_tarea(e):
            nonlocal year_seleccionado, month_seleccionado, day_seleccionado,calendario_cambiado,tarea_selecionada_completa
            overlay_carga.visible = True
            page.update()
            try:
                id_voluntario_Asignado_1=None
                id_voluntario_Asignado_2=None
                id_voluntario_Asignado_3=None
                id_voluntario_Asignado_4=None
                id_voluntario_Asignado_5=None
                voluntarios_asignados=0
                
                bandera=True
                
                # los 3 proximos if's
                # si no se cambia la fecha del calendario
                # si no se cambia el turno
                # si al cambiar el numero de voluntarios lo nuevo es >= a los que habia inicialmente
                # solo si se cumplen las 3 condiciones se activa la bandera=False, con lo cual no se borraran los 
                # voluntarios asignados.
                # si no se cumple alguna de las condiciones se eliminan lo posibles voluntarios que ya se habian asignado porque
                # puede que ya no cumplan las condiciones para la tarea modificada
                if not calendario_cambiado:
                    year_seleccionado=tarea_selecionada_completa['year']
                    month_seleccionado=tarea_selecionada_completa['month']
                    day_seleccionado=tarea_selecionada_completa['day']
                    if lista_turnos.value == tarea_selecionada_completa["turno"]:
                        if int(lista_voluntarios_necesarios.value) >= int(tarea_selecionada_completa["voluntarios_necesarios"]):
                            if check_coordinador.value == tarea_selecionada_completa["coordinador"]: 
                                id_voluntario_Asignado_1=tarea_selecionada_completa["id_voluntario_Asignado_1"]
                                id_voluntario_Asignado_2=tarea_selecionada_completa["id_voluntario_Asignado_2"]
                                id_voluntario_Asignado_3=tarea_selecionada_completa["id_voluntario_Asignado_3"]
                                id_voluntario_Asignado_4=tarea_selecionada_completa["id_voluntario_Asignado_4"]
                                id_voluntario_Asignado_5=tarea_selecionada_completa["id_voluntario_Asignado_5"]
                                voluntarios_asignados=tarea_selecionada_completa["voluntarios_asignados"]
                                
                                bandera=False

            
                    
                
                
                data_tarea = {
                    "id": tarea_selecionada_completa["id"],
                    "user_id": tarea_selecionada_completa["id"],  
                    "tarea_name": edit_tarea.value,  
                    "tarea_ubicacion": edit_ubicacion.value,  
                    "year": year_seleccionado,
                    "month": month_seleccionado,
                    "day": day_seleccionado,
                    "turno": lista_turnos.value,
                    "voluntarios_necesarios": lista_voluntarios_necesarios.value,
                    #"voluntarios_asignados": voluntarios_asignados,
                    "id_voluntario_Asignado_1":id_voluntario_Asignado_1,
                    "id_voluntario_Asignado_2":id_voluntario_Asignado_2,
                    "id_voluntario_Asignado_3":id_voluntario_Asignado_3,
                    "id_voluntario_Asignado_4":id_voluntario_Asignado_4,
                    "id_voluntario_Asignado_5":id_voluntario_Asignado_5,
                    "coordinador":check_coordinador.value
                }

                response=requests.put(f"{API_URL_TAREAS_EDIT}/{tarea_selecionada_completa['id']}",json=data_tarea)
                
                if bandera:
                    #poner a False que el coordinador esta asignado si el usuario es coordinador
                    requests.put(f"{API_URL_TAREAS_EDIT_COORDINADOR}/{tarea_selecionada_completa["id"]}",params={"coordinador_Asignado": False})
                
                    voluntarios_para_borrar=[]
                    for i in range(1,6):
                        voluntario=f"id_voluntario_Asignado_{i}"
                        

                        if tarea_selecionada_completa[voluntario] != None:
                            voluntarios_para_borrar.append(tarea_selecionada_completa[voluntario])
                            

                            
                    for voluntario_para_borrar in voluntarios_para_borrar:
                        borrar_voluntario(e,voluntario_para_borrar)
                if response.status_code==200:
                    texto_snack_bar= f"Se ha modificado correctamente la Tarea {edit_tarea.value} del dia {day_seleccionado}/{month_seleccionado}/{year_seleccionado}"
                    para_atras(e)
                else:
                    texto_snack_bar="No se ha modificado correctamente la Tarea, asegurese de que nombre de Tarea y Ubicacion tengan minimo 3 caracteres"
                snack_bar = ft.SnackBar(content=ft.Text(texto_snack_bar))
                page.overlay.append(snack_bar)
                snack_bar.open = True
                page.update()

            finally:
                overlay_carga.visible = False
                page.update()
            




        
        
        def borrar_voluntario(e, id):          

            #poner a False que el coordinador esta asignado si el usuario es coordinador
            response2=requests.get(f"{API_URL_DATOS_USER}/{id}")                
            user_data2=response2.json()
            if user_data2["coordinador"]:
                requests.put(f"{API_URL_TAREAS_EDIT_COORDINADOR}/{tarea_selecionada_completa["id"]}",params={"coordinador_Asignado": False})

                
            params_tarea = {
                "id_voluntario": id
            }

            params_tareaasignada={
                "tarea_id":tarea_selecionada_completa['id'],
                "user_id": id
            }

            requests.put(f"{API_URL_TAREAS_BORRAR}/{tarea_selecionada_completa['id']}", params=params_tarea)
            requests.delete(f"{API_URL_TAREAS_ASIGNADAS}", params=params_tareaasignada)                 
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
            
            actualizar_tabla_voluntarios() 
                
                
        
        def actualizar_tabla_voluntarios():            
            nonlocal id_voluntarios_asignados, voluntarios_asignados, tarea_selecionada_completa
            
            id_voluntarios_asignados = []
            voluntarios_asignados = []
            data_table.rows.clear()
            
            # Actualiza tarea_selecionada_completa para obtener los datos más recientes
            tarea_actualizada = obtener_tarea_completa()
            if tarea_actualizada:                
                tarea_selecionada_completa = tarea_actualizada                
                
                for i in range(1, 6):
                    voluntario = f"id_voluntario_Asignado_{i}"
                    if tarea_selecionada_completa[voluntario] is not None:
                        id_voluntarios_asignados.append(int(tarea_selecionada_completa[voluntario]))
                        
                
                for voluntario_id in id_voluntarios_asignados:
                    response = requests.get(f"{API_URL_LOGIN}/{voluntario_id}")
                    if response.status_code == 200:
                        voluntario_data = response.json()
                        response2=requests.get(f"{API_URL_DATOS_USER}/{voluntario_data["id"]}")                
                        user_data=response2.json()
                        voluntarios_asignados.append(voluntario_data)
                        data_table.rows.append(
                            ft.DataRow(
                                cells=[
                                    ft.DataCell(
                                        ft.Container(
                                            content=ft.Text(voluntario_data["username"], size=16),
                                            padding=ft.padding.all(5),
                                            alignment=ft.alignment.center_left
                                        )
                                    ),
                                    ft.DataCell(
                                        ft.Container(
                                            content=ft.Text(value="C" if user_data["coordinador"] else "V", size=16),
                                            padding=ft.padding.all(5),
                                            alignment=ft.alignment.center_left
                                        )
                                    ),
                                    ft.DataCell(
                                        ft.Row(
                                            controls=[
                                                ft.IconButton(
                                                    ft.icons.DELETE_OUTLINE,
                                                    tooltip="Borrar voluntario",
                                                    icon_color="red",
                                                    on_click=lambda e, id=voluntario_data["id"]: borrar_voluntario(e, id)
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


        
      
            
            
            


        label_tarea=ft.Text(" Tarea: (mínimo 3 caracteres)",size=19, font_family=ft.FontWeight.BOLD)
        edit_tarea=ft.TextField(value=tarea_selecionada_completa["tarea_name"], bgcolor="#FFE6CA", width=400,)
        label_ubicacion=ft.Text(" Ubicación: (mínimo 3 caracteres)",size=19, font_family=ft.FontWeight.BOLD)
        edit_ubicacion=ft.TextField(value=tarea_selecionada_completa["tarea_ubicacion"], bgcolor="#FFE6CA", width=400,)
        calendario=SpanishCalendar(on_date_selected=on_date_selected,selected_date=f"{tarea_selecionada_completa['year']}-{tarea_selecionada_completa['month']}-{tarea_selecionada_completa['day']}")
        
       
        

        label_turno=ft.Text(" Turno:",size=19, font_family=ft.FontWeight.BOLD)
        lista_turnos = ft.Dropdown(
        width=400,
        height=45,
        options=[
            ft.dropdown.Option("Turno 1"),
            ft.dropdown.Option("Turno 2"),
            ft.dropdown.Option("Turno 3"),
            ft.dropdown.Option("Turno 4"),
            ],
        
        hint_style=ft.TextStyle(
            size=14,
            color=ft.colors.BLACK,
            ),
        bgcolor="#FFE6CA",
        border_color=ft.colors.BLACK,
        text_size=15,
        value=tarea_selecionada_completa['turno']
        )

        label_num_voluntarios=ft.Text(" Numero de voluntarios:",size=19, font_family=ft.FontWeight.BOLD)
        lista_voluntarios_necesarios = ft.Dropdown(
            width=400,
            height=45,
            options=[
                ft.dropdown.Option("1"),
                ft.dropdown.Option("2"),
                ft.dropdown.Option("3"),
                ft.dropdown.Option("4"),
                ft.dropdown.Option("5"),
            ],
            
            hint_style=ft.TextStyle(
                size=14,
                color=ft.colors.BLACK,
                
            ),
            bgcolor="#FFE6CA",
            border_color=ft.colors.BLACK,
            text_size=15,
            value=tarea_selecionada_completa['voluntarios_necesarios']
        )

        check_coordinador=ft.Checkbox(label="Necesita coordinador", value=tarea_selecionada_completa["coordinador"], scale=1.35)

        label_voluntarios_Asignados=ft.Text(" Voluntarios asignados:",size=19, font_family=ft.FontWeight.BOLD)
        data_table = ft.DataTable(    
            bgcolor="#FFE6CA",   
            border_radius=5,        
            vertical_lines=ft.border.BorderSide(1, ft.colors.BLUE_GREY_50),
            horizontal_lines=ft.border.BorderSide(1, ft.colors.BLUE_GREY_50),    
            columns=[            
                
                ft.DataColumn(
                    label=ft.Container(
                        content=ft.Text(
                            "Nombre voluntario",
                            color=ft.colors.BLUE_GREY_800,
                            size=13,
                            weight=ft.FontWeight.W_500,
                        ),
                        width=180,
                        
                    ),
                    numeric=False,
                ),
                ft.DataColumn(
                    label=ft.Container(
                        content=ft.Text(
                            "Rango",
                            color=ft.colors.BLUE_GREY_800,
                            size=13,
                            weight=ft.FontWeight.W_500,
                        ),
                        width=60,
                        
                    ),
                    numeric=False,
                ),
                
                ft.DataColumn(
                    label=ft.Container(
                        content=ft.Text(
                            "Eliminar",
                            color=ft.colors.BLUE_GREY_800,
                            size=13,
                            weight=ft.FontWeight.W_500,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        width=70,
                        alignment=ft.alignment.center,
                        
                    ),
                    numeric=False,
                ),
                
                
            ],
            heading_row_height=45,
            data_row_min_height=45,
            data_row_max_height=45,
            column_spacing=20,
            border=ft.border.all(color=ft.colors.BLUE_GREY_800, width=1),
            rows=[]
        )


        

        boton_guardar_tarea=ft.ElevatedButton(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        ft.icons.SAVE,
                        size=35,
                        color="BLACK"
                    ),
                    ft.Text(
                        "Guardar Tarea",
                        size=35,
                        color="BLACK"
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10  # Espacio entre el icono y el texto
            ),
            width=400,
            height=80,
            on_click=guardar_tarea,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=5), 
                bgcolor=ft.colors.GREEN_200,
                side=ft.BorderSide(width=1, color=ft.colors.BLACK),
            ),
        )
        
        actualizar_tabla_voluntarios()



        columna_tarea=ft.Column(controls=[label_tarea, edit_tarea],spacing=1)
        columna_ubicacion=ft.Column(controls=[label_ubicacion, edit_ubicacion],spacing=1)
        columna_turno=ft.Column(controls=[label_turno, lista_turnos],spacing=1)
        columna_voluntarios=ft.Column(controls=[label_num_voluntarios, lista_voluntarios_necesarios],spacing=1)
        coordinador=ft.Container(content=check_coordinador,margin=ft.margin.only(left=30))
        columna_voluntarios_asignados=ft.Column(controls=[label_voluntarios_Asignados, data_table],spacing=1)
        columna_edit1=ft.Column(controls=[columna_tarea, columna_ubicacion, columna_turno, columna_voluntarios, coordinador, columna_voluntarios_asignados], spacing=10)
        columna_calendario=ft.Container(
            content=ft.Column(controls=[calendario]),
            bgcolor="#FFE6CA",
            border_radius=15,
            border=ft.border.all(width=1,color=ft.colors.BLACK),
            padding=0,
            margin=0
            )
        
        columna_edit2=ft.Container(
            content=ft.Column(controls=[columna_calendario,boton_guardar_tarea], 
                              spacing=60,
                              
                              ),
                              margin=ft.margin.only(top=30)
            
        )
        

        contenedor = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[columna_edit1, columna_edit2],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        spacing=60
                    ),
                    
                ],
                
            ),
        
            margin=20
            
        )

        return contenedor


    def para_atras(e): 
        set_selected_tab_index(1)        
        page.go("/admin")            
        

        
    flecha=ft.IconButton(ft.icons.ARROW_BACK, tooltip="Atras", icon_color=ft.colors.BLUE_900, icon_size=30, on_click=para_atras)
    texto_atras=ft.Text(value="Atras", size=25, color=ft.colors.BLUE_900)
    atras=ft.Container(
        content=ft.Row(controls=[flecha,texto_atras]),
        margin=ft.margin.only(left=40, bottom=20)
        )
    titulo=ft.Container(
        content=ft.Text(value="Edición de Tareas", size=40, font_family=ft.FontWeight.BOLD),
        margin=ft.margin.only(left=40)
        )  
    
    fila_cabecera=ft.Container(
        content=ft.Row(controls=[atras, titulo],
                       spacing=200)
    )




    contenedor=montar_contenido_edit()

    pie_info=ft.Container(
        content=ft.Text(value="Al modificar la fecha, el turno o al reducir voluntarios de una tarea, se borraran los voluntarios asignados",
                        size=20,
                        color="RED"),
        margin=ft.margin.only(left=40, top=25)
        )

    contenedo=ft.Container(
        
        content=ft.Column(controls=[fila_cabecera, contenedor, pie_info])
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
                    #margin=ft.margin.only(top=50)  # La imagen comenzará 50px más abajo
                ),
                ft.Container(
                    content=contenedo,
                    expand=True,
                    bgcolor=ft.colors.TRANSPARENT,
                ),
                overlay_carga
            ]
        ),
        expand=True
    )


    
    
    
    

    

    



    
    return ft.View("/admin/edit", controls=[main_container])