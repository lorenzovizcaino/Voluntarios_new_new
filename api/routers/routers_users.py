from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from ..database import get_db
from ..modelopydantic import LoginRequest
from ..models.usuarios import User as ModelUser





routerlogin = APIRouter()





@routerlogin.get("/login", tags=['login'])
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(ModelUser).filter(ModelUser.username == username).first()
    if not user or user.password != password:
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")
    
    
    else:
        return JSONResponse(content={"message": "Login correcto", "id_user": user.id}, status_code=200)



@routerlogin.get("/login/{id}", tags=['login'])
def get_user_id(id: int, db: Session = Depends(get_db)):
    data=db.query(ModelUser).filter(ModelUser.id==id).first()
    if not data:
        return JSONResponse(status_code=404, content={"message":"Recurso no encontrado"})
    else:         
        return JSONResponse(status_code=200, content=jsonable_encoder(data))


@routerlogin.get("/logindatos/{username}", tags=['login'])
def get_user_id(username: str, db: Session = Depends(get_db)):
    data=db.query(ModelUser).filter(ModelUser.username==username).first()
    if not data:
        return JSONResponse(status_code=404, content={"message":"Recurso no encontrado"})
    else:         
        return JSONResponse(status_code=200, content=jsonable_encoder(data))