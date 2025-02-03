"""
Módulo que define los endpoints de la API para gestionar las tareas.
Proporciona rutas para crear, consultar, actualizar y eliminar tareas,
así como gestionar la asignación de voluntarios y coordinadores.
"""

from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi.encoders import jsonable_encoder
from ..models.tareas import Tareas as ModelTareas


# Crear instancia del router
routertareas = APIRouter()


class Tarea(BaseModel):
    """
    Modelo Pydantic que define la estructura de datos para las operaciones
    de tareas. Incluye validaciones de campos.
    """
    id: Optional[int] = None
    user_id: int
    tarea_name: str = Field(min_length=3, max_length=35)  # Nombre con límites de longitud
    tarea_ubicacion: str = Field(min_length=3, max_length=35)  # Ubicación con límites de longitud
    year: int           # Año de la tarea
    month: int         # Mes de la tarea
    day: int          # Día de la tarea
    turno: str        # Turno asignado
    voluntarios_necesarios: int  # Número total de voluntarios requeridos
    voluntarios_asignados: Optional[int] = None  # Número actual de voluntarios
    # IDs de voluntarios asignados (hasta 5)
    id_voluntario_Asignado_1: Optional[int] = None
    id_voluntario_Asignado_2: Optional[int] = None
    id_voluntario_Asignado_3: Optional[int] = None
    id_voluntario_Asignado_4: Optional[int] = None
    id_voluntario_Asignado_5: Optional[int] = None
    coordinador: bool  # Indica si requiere coordinador
    coordinador_Asignado: Optional[bool] = False  # Estado de asignación del coordinador


@routertareas.post('/tareas', tags=['Tareas'])
def create_tarea(tarea: Tarea, db: Session = Depends(get_db)):
    """
    Crea una nueva tarea en el sistema.
    
    Args:
        tarea (Tarea): Datos de la tarea a crear
        db (Session): Sesión de base de datos
    
    Returns:
        JSONResponse: Confirmación de creación o error
    """
    try:
        new_tarea = ModelTareas(**tarea.model_dump())
        db.add(new_tarea)
        db.commit()
        db.refresh(new_tarea)
        return JSONResponse(
            status_code=201,  
            content={
                "message": "Tarea creada correctamente",
                "tarea_id": new_tarea.id
            }
        )
    except Exception as e:
        db.rollback()  
        return JSONResponse(
            status_code=422,
            content={
                "message": "Error al crear la tarea",
                "detail": str(e)
            }
        )


@routertareas.get('/tareas', tags=['Tareas'])
def get_tarea(db: Session = Depends(get_db)):
    """
    Obtiene todas las tareas del sistema.
    
    Args:
        db (Session): Sesión de base de datos
    
    Returns:
        JSONResponse: Lista de todas las tareas
    """
    data = db.query(ModelTareas).all()    
    return JSONResponse(content=jsonable_encoder(data))


@routertareas.get('/tareas/{id}', tags=['Tareas'])
def get_tarea_id(id: int, db: Session = Depends(get_db)):
    """
    Obtiene una tarea específica por su ID.
    
    Args:
        id (int): ID de la tarea
        db (Session): Sesión de base de datos
    
    Returns:
        JSONResponse: Datos de la tarea o mensaje de error si no existe
    """
    data = db.query(ModelTareas).filter(ModelTareas.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={"message": "Recurso no encontrado"})
    else:         
        return JSONResponse(status_code=200, content=jsonable_encoder(data))


@routertareas.delete('/tareas/{id}', tags=['Tareas'])
def delete_tarea(id: int, db: Session = Depends(get_db)):
    """
    Elimina una tarea específica.
    
    Args:
        id (int): ID de la tarea a eliminar
        db (Session): Sesión de base de datos
    
    Returns:
        JSONResponse: Confirmación de eliminación con datos de la tarea eliminada
    """
    data = db.query(ModelTareas).filter(ModelTareas.id == id).first()     
    db.delete(data)
    db.commit()
    return JSONResponse(content={"message": "Se ha eliminado la tarea", "tarea": jsonable_encoder(data)})


@routertareas.put('/tareas/{id}', tags=['Tareas'])
def update_tarea(tarea: Tarea, id: int, id_voluntario: int, db: Session = Depends(get_db)):
    """
    Actualiza una tarea agregando un nuevo voluntario.
    
    Args:
        tarea (Tarea): Datos actualizados de la tarea
        id (int): ID de la tarea
        id_voluntario (int): ID del voluntario a agregar
        db (Session): Sesión de base de datos
    
    Returns:
        JSONResponse: Datos actualizados de la tarea o mensaje de error
    """
    data = db.query(ModelTareas).filter(ModelTareas.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={"message": "Recurso no encontrado"})
    
    # Incrementar contador de voluntarios
    if data.voluntarios_asignados is None:
        data.voluntarios_asignados = 1
    else:        
        data.voluntarios_asignados = data.voluntarios_asignados + 1
    
    # Asignar voluntario al primer espacio disponible
    if data.id_voluntario_Asignado_1 is None:
        data.id_voluntario_Asignado_1 = id_voluntario
    elif data.id_voluntario_Asignado_2 is None:
        data.id_voluntario_Asignado_2 = id_voluntario
    elif data.id_voluntario_Asignado_3 is None:
        data.id_voluntario_Asignado_3 = id_voluntario
    elif data.id_voluntario_Asignado_4 is None:
        data.id_voluntario_Asignado_4 = id_voluntario
    elif data.id_voluntario_Asignado_5 is None:
        data.id_voluntario_Asignado_5 = id_voluntario
    
    db.commit()
    return JSONResponse(status_code=200, content=jsonable_encoder(tarea))


@routertareas.put('/tareasborrarusuario/{id}', tags=['Tareas'])
def update_tarea(id: int, id_voluntario: int, db: Session = Depends(get_db)):
    """
    Elimina un voluntario de una tarea.
    
    Args:
        id (int): ID de la tarea
        id_voluntario (int): ID del voluntario a eliminar
        db (Session): Sesión de base de datos
    
    Returns:
        JSONResponse: Confirmación de eliminación o mensaje de error
    """
    encontrado = False
    data = db.query(ModelTareas).filter(ModelTareas.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={"message": "Recurso no encontrado"})
    
    # Decrementar contador de voluntarios
    data.voluntarios_asignados = data.voluntarios_asignados - 1
    
    # Buscar y eliminar el voluntario de su posición
    if data.id_voluntario_Asignado_1 == str(id_voluntario):
        data.id_voluntario_Asignado_1 = None
        encontrado = True
    elif data.id_voluntario_Asignado_2 == str(id_voluntario):
        data.id_voluntario_Asignado_2 = None
        encontrado = True
    elif data.id_voluntario_Asignado_3 == str(id_voluntario):
        data.id_voluntario_Asignado_3 = None
        encontrado = True
    elif data.id_voluntario_Asignado_4 == str(id_voluntario):
        data.id_voluntario_Asignado_4 = None
        encontrado = True
    elif data.id_voluntario_Asignado_5 == str(id_voluntario):
        data.id_voluntario_Asignado_5 = None
        encontrado = True
    
    db.commit()
    return JSONResponse(
        status_code=200,
        content={"message": "Usuario eliminado correctamente de la tarea"}
    )


@routertareas.put('/tareasedit/{id}', tags=['Tareas'])
def update_tarea(tarea: Tarea, id: int, db: Session = Depends(get_db)):
    """
    Actualiza los datos generales de una tarea.
    
    Args:
        tarea (Tarea): Nuevos datos de la tarea
        id (int): ID de la tarea a actualizar
        db (Session): Sesión de base de datos
    
    Returns:
        JSONResponse: Datos actualizados de la tarea o mensaje de error
    """
    data = db.query(ModelTareas).filter(ModelTareas.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={"message": "Recurso no encontrado"})
    
    # Actualizar todos los campos de la tarea
    data.tarea_name = tarea.tarea_name
    data.tarea_ubicacion = tarea.tarea_ubicacion
    data.turno = tarea.turno
    data.voluntarios_necesarios = tarea.voluntarios_necesarios
    data.day = tarea.day
    data.month = tarea.month
    data.year = tarea.year
    data.id_voluntario_Asignado_1 = tarea.id_voluntario_Asignado_1
    data.id_voluntario_Asignado_2 = tarea.id_voluntario_Asignado_2
    data.id_voluntario_Asignado_3 = tarea.id_voluntario_Asignado_3
    data.id_voluntario_Asignado_4 = tarea.id_voluntario_Asignado_4
    data.id_voluntario_Asignado_5 = tarea.id_voluntario_Asignado_5
    data.coordinador = tarea.coordinador
    
    db.commit()
    return JSONResponse(status_code=200, content=jsonable_encoder(tarea))


@routertareas.put('/tareaseditcoordinador/{id}', tags=['Tareas'])
async def update_tarea(id: int, coordinador_Asignado: bool = Query(...), db: Session = Depends(get_db)):
    """
    Actualiza el estado de asignación del coordinador de una tarea.
    
    Args:
        id (int): ID de la tarea
        coordinador_Asignado (bool): Nuevo estado de asignación del coordinador
        db (Session): Sesión de base de datos
    
    Returns:
        JSONResponse: Confirmación de actualización o mensaje de error
    """
    try:
        data = db.query(ModelTareas).filter(ModelTareas.id == id).first()
        if not data:
            return JSONResponse(status_code=404, content={"message": "Recurso no encontrado"})
        
        data.coordinador_Asignado = coordinador_Asignado
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Actualizado correctamente"})
    
    except Exception as e:
        db.rollback()
        print(f"Error: {str(e)}")  
        return JSONResponse(status_code=500, content={"message": "Error interno del servidor"})