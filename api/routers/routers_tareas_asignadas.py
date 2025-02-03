"""
Módulo que define los endpoints de la API para gestionar la asignación de tareas a usuarios.
Proporciona rutas para crear, consultar y eliminar las relaciones entre tareas y usuarios.
"""

from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi.encoders import jsonable_encoder
from ..models.tareas_asignadas import TareasAsignadas as ModelTareasAsignadas


# Crear instancia del router
routertareas_asignadas = APIRouter()


class TareaAsignada(BaseModel):
    """
    Modelo Pydantic que define la estructura de datos para las operaciones
    de asignación de tareas.
    """
    id: Optional[int] = None  # ID opcional para creación/actualización
    tarea_id: int            # ID de la tarea a asignar
    user_id: int            # ID del usuario al que se asigna la tarea


@routertareas_asignadas.post('/tareasasignadas', tags=['TareasAsignadas'])
def create_tarea(tarea_asignada: TareaAsignada, db: Session = Depends(get_db)):
    """
    Crea una nueva asignación de tarea a usuario.
    
    Args:
        tarea_asignada (TareaAsignada): Datos de la asignación
        db (Session): Sesión de base de datos
    
    Returns:
        JSONResponse: Confirmación de creación o error
    """
    try:
        new_tarea = ModelTareasAsignadas(**tarea_asignada.model_dump())
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
                "message": "Error al crear la tarea asignada",
                "detail": str(e)
            }
        )


@routertareas_asignadas.get('/tareasasignadas/{user_id}', tags=['TareasAsignadas'])
def tareas_usuario(user_id: int, db: Session = Depends(get_db)):
    """
    Obtiene todas las tareas asignadas a un usuario específico.
    
    Args:
        user_id (int): ID del usuario
        db (Session): Sesión de base de datos
    
    Returns:
        JSONResponse: Lista de tareas asignadas al usuario
    """
    try:
        data = db.query(ModelTareasAsignadas).filter(
            ModelTareasAsignadas.user_id == user_id
        ).all()
        
        return JSONResponse(
            status_code=200,
            content={
                "user_id": user_id,
                "tareas": jsonable_encoder(data)
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message": "Error al listar tareas del usuario {user_id}",
                "detail": str(e)
            }
        )


@routertareas_asignadas.get('/usersasignados/{tarea_id}', tags=['TareasAsignadas'])
def usuario_tareas(tarea_id: int, db: Session = Depends(get_db)):
    """
    Obtiene todos los usuarios asignados a una tarea específica.
    
    Args:
        tarea_id (int): ID de la tarea
        db (Session): Sesión de base de datos
    
    Returns:
        JSONResponse: Lista de usuarios asignados a la tarea
    """
    try:
        data = db.query(ModelTareasAsignadas).filter(
            ModelTareasAsignadas.tarea_id == tarea_id
        ).all()
        
        return JSONResponse(
            status_code=200,
            content={
                "users": jsonable_encoder(data)
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message": "Error al listar usuarios de una tarea {tarea_id}",
                "detail": str(e)
            }
        )


@routertareas_asignadas.get('/tareasasignadas/{user_id}/count', tags=['TareasAsignadas'])
def count_tareas_usuario(user_id: int, db: Session = Depends(get_db)):
    """
    Cuenta el número total de tareas asignadas a un usuario.
    
    Args:
        user_id (int): ID del usuario
        db (Session): Sesión de base de datos
    
    Returns:
        JSONResponse: Total de tareas asignadas al usuario
    """
    try:
        count = db.query(ModelTareasAsignadas).filter(
            ModelTareasAsignadas.user_id == user_id
        ).count()
        
        return JSONResponse(
            status_code=200,
            content={
                "user_id": user_id,
                "total_tareas": count
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message": "Error al contar tareas",
                "detail": str(e)
            }
        )


@routertareas_asignadas.delete('/tareasasignadas/{tarea_id}', tags=['TareasAsignadas'])
def delete_tarea_asignada(tarea_id: int, db: Session = Depends(get_db)):
    """
    Elimina todas las asignaciones asociadas a una tarea específica.
    
    Args:
        tarea_id (int): ID de la tarea
        db (Session): Sesión de base de datos
    
    Returns:
        JSONResponse: Confirmación de eliminación
    """
    # Para borrar más de un registro se utiliza delete() en lugar de all()
    data = db.query(ModelTareasAsignadas).filter(ModelTareasAsignadas.tarea_id == tarea_id).delete()
    db.commit()
    return JSONResponse(content={"message": "Se ha eliminado la/s tarea/s asignada/s"})


@routertareas_asignadas.delete('/tareasasignadas', tags=['TareasAsignadas'])
def delete_tarea_asignada(tarea_id: int, user_id: int, db: Session = Depends(get_db)):
    """
    Elimina una asignación específica de tarea a usuario.
    
    Args:
        tarea_id (int): ID de la tarea
        user_id (int): ID del usuario
        db (Session): Sesión de base de datos
    
    Returns:
        JSONResponse: Confirmación de eliminación
    """
    db.query(ModelTareasAsignadas).filter(
        (ModelTareasAsignadas.tarea_id == tarea_id) & 
        (ModelTareasAsignadas.user_id == user_id)
    ).delete()
    db.commit()
    return JSONResponse(content={"message": "Se ha eliminado la tarea asignada"})