import flet as ft
import requests
from admin_view import tarea_para_asignar
from utils import API_URL_TAREAS, get_id_usuario_logeado, API_URL_TURNOS_DISPONIBLES, API_URL_LOGIN, API_URL_TAREAS_ASIGNADAS, API_URL_DATOS_USER, API_URL_TAREAS_EDIT_COORDINADOR, set_selected_tab_index,path_fondo, obtener_tarea_completa
from enviar_email import enviar_correo



def admin_assign(page: ft.Page):
    page.window_width = 800
    page.window_height = 900  
    page.window_center()
    
    page.title="Tareas de Voluntariado"
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
    texto_info=""
    tarea_selecionada_completa=None
    coordinador_ingresado=False

    
        

    """
    la siguiente funcion obtiene los id de todos los usuarios de la base de datos que son validos para
    la tarea que se esta evaluando en el momento, para ello tiene en cuenta:
        1.- Que el usuario haya marcado la fecha y el turno en cuestion  como disponible.
        2.- Que el usuario no tenga asignada ya una tarea para el mismo dia.
    """    
    def obtener_id_voluntarios_disponibles(tarea_selecionada_completa):
        nonlocal coordinador_ingresado
        
        
        usuarios=[] 
        usuariosfinales=[]      
        id_tareas_usuario=[] 
        data={
            "year":tarea_selecionada_completa["year"],
            "month":tarea_selecionada_completa["month"],
            "day":tarea_selecionada_completa["day"],
            "turno":tarea_selecionada_completa["turno"]

        }

        

        #se comprueba que usuario estan disponibles en la fecha de la tarea que estamos asignando y que si hace falta un coordinador
        #y este ya ha sido asignado ya no aparezcan el resto de coordinadores aunque esten disponibles para la tarea
        try:
            response=requests.get(API_URL_TURNOS_DISPONIBLES, params=data)
            if response.status_code==200:
                
                usuarios_disponibles=response.json()
                for user in usuarios_disponibles:
                    response2=requests.get(f"{API_URL_TAREAS}/{tarea_selecionada_completa['id']}")
                    tarea_consulta=response2.json()
                    
                    coordinador_ingresado=tarea_consulta["coordinador_Asignado"]
                    
                    if tarea_selecionada_completa["coordinador"] and  coordinador_ingresado==False:                    
                        usuarios.append(user["user_id"])
                        
                    else:                                      
                        response2=requests.get(f"{API_URL_DATOS_USER}/{user['user_id']}")                
                        user_data2=response2.json()
                        if user_data2["coordinador"]==False:
                            usuarios.append(user["user_id"])

                        

                
            else:
                print(f"Error al obtener datos: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error en la conexión: {str(e)}")
            return None
        
        
        
        usuariosfinales=usuarios.copy()
        
        #se comprueba que los usuarios que tienen la fecha selecionada no tengan ya otra tarea para ese mismo dia
        #1º se obtienen todas las tareas de cada usuario
        for user in usuarios:
            try:
                
                response=requests.get(f"{API_URL_TAREAS_ASIGNADAS}/{user}")
                if response.status_code==200:                    
                    data = response.json()
                    tareas_usuario = data["tareas"]  
                    id_tareas_usuario.clear()
                    for tarea in tareas_usuario:
                        id_tareas_usuario.append(tarea["tarea_id"])
                    

                    
                else:
                    print(f"Error al obtener datos: {response.status_code}")
                    return None
                
            except Exception as e:
                print(f"Error en la conexión: {str(e)}")
                return None
            
            #2º por cada tarea del usuario hay que comprobar que no coincida en fecha con la tarea actual
            for id_tarea in id_tareas_usuario:
                try:
                    response=requests.get(f"{API_URL_TAREAS}/{id_tarea}")
                    if response.status_code==200:                    
                        data = response.json()
                        year=data["year"]
                        month=data["month"]
                        day=data["day"]
                        fecha=f"{day}/{month}/{year}"
                        
                        if fecha==tarea_para_asignar.tarea_seleccionada['fecha']:
                        #si el mismo dia ya tiene una tarea asignada se elimina el usuario para la tarea que estamos evaluando ahora
                            usuariosfinales.remove(user)
                            break

                        

                        
                    else:
                        print(f"Error al obtener datos: {response.status_code}")
                        return None
                    
                except Exception as e:
                    print(f"Error en la conexión: {str(e)}")
                    return None

        if len(usuariosfinales)==0:
            info.value="No hay voluntarios disponibles para esta tarea"
        return usuariosfinales

        

        

        

    def obtener_voluntarios_disponibles(id_voluntarios_disponibles):
        usuarios_disponibles=[]
        for user in id_voluntarios_disponibles:            
            response=requests.get(f"{API_URL_LOGIN}/{user}")
            usuarios_disponibles.append(response.json())
        
        return usuarios_disponibles
    
    def asignar_tarea(e, dato):
        
        nonlocal tarea_selecionada_completa, voluntarios_disponibles
        
        #poner a True que el coordinador esta asignado si el usuario es coordinador
        response2=requests.get(f"{API_URL_DATOS_USER}/{dato["id"]}")                
        user_data2=response2.json()
        if user_data2["coordinador"]:
            requests.put(f"{API_URL_TAREAS_EDIT_COORDINADOR}/{tarea_selecionada_completa["id"]}",params={"coordinador_Asignado": True})



        data_tarea = {
                "id": tarea_selecionada_completa["id"],
                "user_id": tarea_selecionada_completa["id"],  
                "tarea_name": tarea_selecionada_completa["tarea_name"],  
                "tarea_ubicacion": tarea_selecionada_completa["tarea_ubicacion"],  
                "year": tarea_selecionada_completa["year"],
                "month": tarea_selecionada_completa["month"],
                "day": tarea_selecionada_completa["day"],
                "turno": tarea_selecionada_completa["turno"],
                "voluntarios_necesarios": tarea_selecionada_completa["voluntarios_necesarios"],
                "coordinador": tarea_selecionada_completa["coordinador"]
            }


        params_tarea={
            "id":tarea_selecionada_completa["id"],
            "id_voluntario":dato["id"]
        }

        data_tarea_asignada={
            "tarea_id":tarea_selecionada_completa["id"],
            "user_id":dato["id"]

        }
        

        response=requests.put(f"{API_URL_TAREAS}/{tarea_selecionada_completa['id']}",json=data_tarea, params=params_tarea)
        response2=requests.post(API_URL_TAREAS_ASIGNADAS, json=data_tarea_asignada)
        asunto=f"Nueva tarea de voluntariado asignada el dia {tarea_selecionada_completa["day"]}/{tarea_selecionada_completa["month"]}/{tarea_selecionada_completa["year"]}"
        mensaje=f"""
                Estimado voluntario:
                Se le ha asignado una nueva tarea:
                TAREA: {tarea_selecionada_completa["tarea_name"]}
                UBICACION: {tarea_selecionada_completa["tarea_ubicacion"]}
                DIA: {tarea_selecionada_completa["day"]}/{tarea_selecionada_completa["month"]}/{tarea_selecionada_completa["year"]}

                Muchas gracias por su colaboracion
                """

        enviar_correo("antoniosantaballa@gmail.com",asunto, mensaje)

        tarea_selecionada_completa=obtener_tarea_completa(tarea_para_asignar.tarea_seleccionada["id"])
        
        tarea_para_asignar.tarea_seleccionada['voluntarios_asignados']=tarea_selecionada_completa['voluntarios_asignados']
                

        id_voluntarios_disponibles = obtener_id_voluntarios_disponibles(tarea_selecionada_completa)
        if id_voluntarios_disponibles is not None:
            voluntarios_disponibles = obtener_voluntarios_disponibles(id_voluntarios_disponibles)

        # Actualizar los elementos visuales
        vol_asignados.value = f"VOLUNTARIOS ASIGNADOS: {tarea_selecionada_completa['voluntarios_asignados']}"
        actualizar_tabla()
        
        
    def comprobar_duplicidad_usuario_tarea(id_usuario): 
        usuarios_tarea=[]
        response=requests.get(f"{API_URL_TAREAS}/{tarea_para_asignar.tarea_seleccionada['id']}")
        tarea=response.json()
        for i in range (1,6):
            if not tarea[f"id_voluntario_Asignado_{i}"] == None:
                usuarios_tarea.append(tarea[f"id_voluntario_Asignado_{i}"])
        if str(id_usuario) in usuarios_tarea:
            return True
        else:
            return False
        
          

        
    def actualizar_tabla():
        
        data_table.rows.clear()
        if tarea_para_asignar.tarea_seleccionada['voluntarios_necesarios']==tarea_para_asignar.tarea_seleccionada['voluntarios_asignados']:
            info.value="Esta tarea ya tiene todos los voluntarios necesarios"
        else:

            for dato in voluntarios_disponibles:
                #dato es cada uno de los voluntarios disponibles            
                response_contar=requests.get(f"{API_URL_TAREAS_ASIGNADAS}/{dato["id"]}/count")
                numero_tareas=response_contar.json()
                               
                response2=requests.get(f"{API_URL_DATOS_USER}/{dato["id"]}")                
                user_data2=response2.json()
                coordinador="Si" if user_data2["coordinador"] else "No"
                duplica_usuario_tarea=comprobar_duplicidad_usuario_tarea(dato["id"])                
                if duplica_usuario_tarea:                    
                    continue


                data_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(
                                ft.Container(
                                    content=ft.Text(dato["username"], size=16), 
                                    width=130,
                                    padding=ft.padding.all(5),
                                    
                                )
                            ),

                            ft.DataCell(
                                ft.Container(
                                    content=ft.Text(value=coordinador, size=16), 
                                    width=100,
                                    padding=ft.padding.all(5),
                                    
                                )
                            ),
                            ft.DataCell(
                                ft.Container(
                                    content=ft.Text(
                                        str(numero_tareas["total_tareas"]),
                                        size=16,
                                        text_align=ft.TextAlign.CENTER,
                                    ),
                                    width=90,
                                    alignment=ft.alignment.center,
                                    padding=ft.padding.all(5),
                                )
                            ),
                        
                            ft.DataCell(
                                ft.Container(
                                    content=ft.IconButton(
                                        ft.icons.ACCESS_TIME,
                                        tooltip="Asignar",
                                        icon_color="blue",
                                        on_click=lambda e, dato=dato: asignar_tarea(e, dato)
                                    ),
                                    width=120,
                                    alignment=ft.alignment.center,
                                    padding=ft.padding.all(5),
                                )
                            ),
                        ]
                    )
                )
        
        page.update()

    def para_atras(e): 
        set_selected_tab_index(1)        
        page.go("/admin")


  
        
        
        
            
            

            
        

      
    flecha=ft.IconButton(ft.icons.ARROW_BACK, tooltip="Atras", icon_color=ft.colors.BLUE_900, icon_size=30, on_click=para_atras)
    texto_atras=ft.Text(value="Atras", size=20, color=ft.colors.BLUE_900)
    atras=ft.Row(controls=[flecha,texto_atras])
    titulo=ft.Text(value="Asignacion de Tareas", size=25, font_family=ft.FontWeight.BOLD)
    tarea=ft.Text(value=f"TAREA: {tarea_para_asignar.tarea_seleccionada['nombre']}")
    ubicacion=ft.Text(value=f"UBICACIÓN: {tarea_para_asignar.tarea_seleccionada['ubicacion']}")
    fecha=ft.Text(value=f"FECHA: {tarea_para_asignar.tarea_seleccionada['fecha']}")
    turno=ft.Text(value=f"TURNO: {tarea_para_asignar.tarea_seleccionada['turno']}")    
    coordinador = ft.Text(value=f"NECESITA COORDINADOR: {'Si' if tarea_para_asignar.tarea_seleccionada['coordinador'] else 'No'}")
    vol_necesarios=ft.Text(value=f"VOLUNTARIOS NECESARIOS: {tarea_para_asignar.tarea_seleccionada['voluntarios_necesarios']}")
    vol_asignados=ft.Text(value=f"VOLUNTARIOS ASIGNADOS: {tarea_para_asignar.tarea_seleccionada['voluntarios_asignados']} ")
    columna_tarea=ft.Column(controls=[tarea, ubicacion,fecha,turno,coordinador,vol_necesarios,vol_asignados])
    subtitulo=ft.Text(value="Voluntarios disponibles", size=20, font_family=ft.FontWeight.BOLD)

   

    



    data_table = ft.DataTable(    
        bgcolor=ft.colors.with_opacity(0.8, ft.colors.RED_50),      
        border_radius=8,        
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
                    width=130,
                    padding=ft.padding.all(5),
                ),
                numeric=False,
            ),

            ft.DataColumn(
                label=ft.Container(
                    content=ft.Text(
                        "Coordinador",
                        color=ft.colors.BLUE_GREY_800,
                        size=13,
                        weight=ft.FontWeight.W_500,
                    ),
                    width=100,
                    padding=ft.padding.all(5),
                ),
                numeric=False,
            ),
            
            ft.DataColumn(
                label=ft.Container(
                    content=ft.Text(
                        "Tareas acumuladas",
                        color=ft.colors.BLUE_GREY_800,
                        size=13,
                        weight=ft.FontWeight.W_500,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    width=90,
                    alignment=ft.alignment.center,
                    padding=ft.padding.all(5),
                ),
                numeric=False,
            ),
            
            ft.DataColumn(
                label=ft.Container(
                    content=ft.Text(
                        "Asignar",
                        color=ft.colors.BLUE_GREY_800,
                        size=13,
                        weight=ft.FontWeight.W_500,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    width=120,
                    alignment=ft.alignment.center,
                    padding=ft.padding.all(5),
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
        height=370, 
    )

    contenedor_tabla = ft.Container(
        content=tabla_con_scroll,
        width=750,        
        padding=0,
    )













    info=ft.Text(value=texto_info, 
                 color=ft.colors.BLACK, 
                 size=20, 
                 weight=ft.FontWeight.BOLD, 
                 text_align=ft.TextAlign.CENTER)
    
    container_info=ft.Container(
        content=info,
        bgcolor=ft.colors.with_opacity(0.8, ft.colors.RED_50),
        width=750,
        height=50,padding=5,
        border_radius=5,
        border=ft.border.all(width=1,color=ft.colors.BLACK),
        alignment=ft.alignment.center
    )


    tarea_selecionada_completa=obtener_tarea_completa(tarea_para_asignar.tarea_seleccionada["id"])
    id_voluntarios_disponibles=obtener_id_voluntarios_disponibles(tarea_selecionada_completa)
    if not id_voluntarios_disponibles ==  None:    
        voluntarios_disponibles=obtener_voluntarios_disponibles(id_voluntarios_disponibles)
        actualizar_tabla()
        page.update()
    else:
        print("No hay voluntarios disponibles para esa tarea")
        info.value="No hay voluntarios disponibles para esa tarea"
        page.update()



    contenedor=ft.Container(
        content=ft.Column(
            controls=[atras,titulo, columna_tarea, subtitulo, contenedor_tabla,  ] + ([container_info] if info.value != "" else [])  # Añade container_info solo si hay valor
        ),
        padding=30
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
                    #margin=ft.margin.only(top=50)  
                ),
                ft.Container(
                    content=contenedor,
                    expand=True,
                    bgcolor=ft.colors.TRANSPARENT,
                )
            ]
        ),
        expand=True
    )


    
    
    
    

    

    



    
    return ft.View("/admin/assign", controls=[main_container])