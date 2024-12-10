from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from ..database import get_db
#from ..modelopydantic import TurnosRequest
from ..models.usuarios import User as ModelUser
from ..models.turnos import Turnos as ModelTurnos






routerturnos = APIRouter()

class Turno(BaseModel):
    id: Optional[int]=None
    user_id:int
    year:int
    month:int
    day:int
    turno1:bool=False
    turno2:bool=False
    turno3:bool=False
    turno4:bool=False






# METODOS HTTP
# POST: Crear un recurso nuevo.
# PUT: Modificar un recurso existente.
# GET: Consultar informacion de un recurso.
# DELETE: Eliminar un recurso




@routerturnos.post('/turnos', tags=['Turnos'])
def create_turno(turno: Turno, db: Session = Depends(get_db)):
    new_turno = ModelTurnos(**turno.model_dump())    
    db.add(new_turno)
    db.commit()
    return JSONResponse(content={"message": "Se ha añadido un nuevo turno"})




@routerturnos.get('/turnosdisponibles', tags=['Turnos_Disponibles'])
def consultar_id_disponibles(year: int, month: int, day: int, turno: str, db: Session = Depends(get_db)):
    turnos_map = {
        "Turno 1": ModelTurnos.turno1,
        "Turno 2": ModelTurnos.turno2,
        "Turno 3": ModelTurnos.turno3,
        "Turno 4": ModelTurnos.turno4
    }

    turno_field = turnos_map.get(turno)
    data=db.query(ModelTurnos).filter(
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
    turnos_map = {
        0: ModelTurnos.turno1,
        1: ModelTurnos.turno2,
        2: ModelTurnos.turno3,
        3: ModelTurnos.turno4
    }

    turno_field = turnos_map.get(checkbox)
    
    if turno_field is None:
        return JSONResponse(status_code=400, content={"message": "Checkbox inválido"})
    
    print(f"checkbox: {checkbox}")
    data = db.query(ModelTurnos).filter(
        ModelTurnos.user_id == user_id,
        ModelTurnos.year ==year,
        ModelTurnos.month == month,
        ModelTurnos.day== day,
        turno_field == True
    ).first()

    if data:
        return JSONResponse(status_code=200, content={"message": "Existe"})
    else:
        return JSONResponse(status_code=422, content={"message": "NO Existe"})








@routerturnos.delete('/turnos', tags=['Turnos'])
def delete_turno(turno: Turno, db: Session = Depends(get_db)):
    data = db.query(ModelTurnos).filter(
        ModelTurnos.user_id == turno.user_id,
        ModelTurnos.year ==turno.year,
        ModelTurnos.month == turno.month,
        ModelTurnos.day== turno.day,
        ModelTurnos.turno1 == turno.turno1,
        ModelTurnos.turno2 == turno.turno2,
        ModelTurnos.turno3 == turno.turno3,
        ModelTurnos.turno4 == turno.turno4,
    ).first()
    db.delete(data)
    db.commit()
    return JSONResponse(content={"message":"Se ha eliminado un turno"})




