"""
Módulo que define los endpoints de la API para gestionar los turnos.
Este módulo permite crear, consultar y eliminar turnos, así como verificar
la disponibilidad de usuarios en diferentes turnos y fechas.
"""

from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from ..database import get_db
from ..models.usuarios import User as ModelUser
from ..models.turnos import Turnos as ModelTurnos


# Crear instancia del router
routerturnos = APIRouter()


class Turno(BaseModel):
    """
    Modelo Pydantic que define la estructura de datos para las operaciones
    de turnos. Gestiona la disponibilidad de un usuario en diferentes
    turnos para una fecha específica.
    """
    id: Optional[int] = None       # Identificador único del turno
    user_id: int                   # ID del usuario asociado al turno
    year: int                      # Año del turno
    month: int                     # Mes del turno
    day: int                       # Día del turno
    turno1: bool = False          # Disponibilidad para el primer turno
    turno2: bool = False          # Disponibilidad para el segundo turno
    turno3: bool = False          # Disponibilidad para el tercer turno
    turno4: bool = False          # Disponibilidad para el cuarto turno


@routerturnos.post('/turnos', tags=['Turnos'])
def create_turno(turno: Turno, db: Session = Depends(get_db)):
    """
    Crea un nuevo registro de turno en el sistema.
    
    Args:
        turno (Turno): Datos del turno a crear
        db (Session): Sesión de base de datos
    
    Returns:
        JSONResponse: Confirmación de creación del turno
    """
    new_turno = ModelTurnos(**turno.model_dump())    
    db.add(new_turno)
    db.commit()
    return JSONResponse(content={"message": "Se ha añadido un nuevo turno"})


@routerturnos.get('/turnosdisponibles', tags=['Turnos_Disponibles'])
def consultar_id_disponibles(year: int, month: int, day: int, turno: str, db: Session = Depends(get_db)):
    """
    Consulta los usuarios disponibles para un turno específico en una fecha determinada.
    
    Args:
        year (int): Año de la consulta
        month (int): Mes de la consulta
        day (int): Día de la consulta
        turno (str): Turno específico a consultar ("Turno 1", "Turno 2", etc.)
        db (Session): Sesión de base de datos
    
    Returns:
        JSONResponse: Lista de usuarios disponibles o mensaje de error
    """
    # Mapeo de nombres de turno a campos del modelo
    turnos_map = {
        "Turno 1": ModelTurnos.turno1,
        "Turno 2": ModelTurnos.turno2,
        "Turno 3": ModelTurnos.turno3,
        "Turno 4": ModelTurnos.turno4
    }

    turno_field = turnos_map.get(turno)
    data = db.query(ModelTurnos).filter(
        ModelTurnos.year == year,
        ModelTurnos.month == month,
        ModelTurnos.day == day, 
        turno_field == True
    ).all()

    if data:
        return JSONResponse(status_code=200, content=jsonable_encoder(data))
    else:
        return JSONResponse(status_code=422, content={"message": "NO Existe"})


@routerturnos.get('/turnos', tags=['Turnos'])
def consultar_turno(user_id: int, year: int, month: int, day: int, checkbox: int, db: Session = Depends(get_db)):
    """
    Verifica la disponibilidad de un usuario en un turno específico.
    
    Args:
        user_id (int): ID del usuario a consultar
        year (int): Año de la consulta
        month (int): Mes de la consulta
        day (int): Día de la consulta
        checkbox (int): Índice del turno (0-3)
        db (Session): Sesión de base de datos
    
    Returns:
        JSONResponse: Confirmación de disponibilidad o mensaje de error
    """
    # Mapeo de índices de checkbox a campos del modelo
    turnos_map = {
        0: ModelTurnos.turno1,
        1: ModelTurnos.turno2,
        2: ModelTurnos.turno3,
        3: ModelTurnos.turno4
    }

    turno_field = turnos_map.get(checkbox)
    
    if turno_field is None:
        return JSONResponse(status_code=400, content={"message": "Checkbox inválido"})
    
    data = db.query(ModelTurnos).filter(
        ModelTurnos.user_id == user_id,
        ModelTurnos.year == year,
        ModelTurnos.month == month,
        ModelTurnos.day == day,
        turno_field == True
    ).first()

    if data:
        return JSONResponse(status_code=200, content={"message": "Existe"})
    else:
        return JSONResponse(status_code=422, content={"message": "NO Existe"})


@routerturnos.delete('/turnos', tags=['Turnos'])
def delete_turno(turno: Turno, db: Session = Depends(get_db)):
    """
    Elimina un registro de turno específico.
    
    Args:
        turno (Turno): Datos del turno a eliminar
        db (Session): Sesión de base de datos
    
    Returns:
        JSONResponse: Confirmación de eliminación
    """
    data = db.query(ModelTurnos).filter(
        ModelTurnos.user_id == turno.user_id,
        ModelTurnos.year == turno.year,
        ModelTurnos.month == turno.month,
        ModelTurnos.day == turno.day,
        ModelTurnos.turno1 == turno.turno1,
        ModelTurnos.turno2 == turno.turno2,
        ModelTurnos.turno3 == turno.turno3,
        ModelTurnos.turno4 == turno.turno4,
    ).first()
    db.delete(data)
    db.commit()
    return JSONResponse(content={"message": "Se ha eliminado un turno"})