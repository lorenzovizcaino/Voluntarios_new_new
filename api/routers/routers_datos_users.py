from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from ..database import get_db
from ..modelopydantic import LoginRequest
from ..models.datos_usuarios import  DatosUser as ModelDatosUser





routerdatosuser = APIRouter()

class Datos_User(BaseModel):
    id: Optional[int]=None
    user_id:int
    email: str
    direccion: str
    telefono: str
    chat_id: str
    tipo_usuario: str
    config: bool
    coordinador: bool=False
    amigo: str





@routerdatosuser.get('/datosuser/{id}', tags=['datos_user'])
def get_datos_user(id:int, db:Session=Depends(get_db)):
    
    data=db.query(ModelDatosUser).filter(ModelDatosUser.id==id).first()
    if not data:
        return JSONResponse(status_code=404, content={"message":"Recurso no encontrado"})
    else:         
        return JSONResponse(status_code=200, content=jsonable_encoder(data))