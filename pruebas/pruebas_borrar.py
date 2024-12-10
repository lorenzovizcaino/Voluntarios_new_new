import flet as ft

def main(page: ft.Page):
    page.title = "Ejemplo de Tabla con Acciones"
    
    # Datos iniciales de la tabla
    datos = [
        {"id": 1, "nombre": "Juan", "edad": 25},
        {"id": 2, "nombre": "María", "edad": 30},
        {"id": 3, "nombre": "Pedro", "edad": 35},
    ]
    print(datos)
    # Crear tabla
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Edad")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[]
    )
    
    def borrar_fila(e, id):
        # Encontrar y eliminar la fila con el ID correspondiente
        for i, dato in enumerate(datos):
            if dato["id"] == id:
                datos.pop(i)
                actualizar_tabla()
                break
        page.update()
    
    def editar_fila(e, id):
        # Aquí puedes implementar la lógica de edición
        # Por ejemplo, mostrar un diálogo con campos para editar
        dlg = ft.AlertDialog(
            title=ft.Text(f"Editar registro {id}"),
            content=ft.Text("Aquí irían los campos de edición")
        )
        page.dialog = dlg
        dlg.open = True
        page.update()
    
    def actualizar_tabla():
        # Limpiar filas existentes
        tabla.rows.clear()
        
        # Agregar filas con datos actualizados
        for dato in datos:
            tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(dato["id"]))),
                        ft.DataCell(ft.Text(dato["nombre"])),
                        ft.DataCell(ft.Text(str(dato["edad"]))),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.IconButton(
                                        ft.icons.DELETE_OUTLINE,
                                        tooltip="Borrar",
                                        icon_color="red",
                                        on_click=lambda e, id=dato["id"]: borrar_fila(e, id)
                                    ),
                                    ft.IconButton(
                                        ft.icons.EDIT,
                                        tooltip="Editar",
                                        icon_color="blue",
                                        on_click=lambda e, id=dato["id"]: editar_fila(e, id)
                                    ),
                                ]
                            )
                        ),
                    ]
                )
            )
    
    # Inicializar tabla con datos
    actualizar_tabla()
    
    # Agregar tabla a la página
    page.add(tabla)
    page.update()

ft.app(target=main)