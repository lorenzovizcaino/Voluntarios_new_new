"""
Módulo que define los endpoints de la API para la autenticación y consulta
de usuarios. Proporciona rutas para el login y la obtención de información
de usuarios por diferentes criterios.
"""

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


# Crear instancia del router para operaciones de login
routerlogin = APIRouter()


@routerlogin.get("/login", tags=['login'])
def login(username: str, password: str, db: Session = Depends(get_db)):
    """
    Endpoint para autenticar usuarios en el sistema.
    
    Verifica las credenciales proporcionadas contra la base de datos y
    retorna el ID del usuario si la autenticación es exitosa.
    
    Args:
        username (str): Nombre de usuario
        password (str): Contraseña del usuario
        db (Session): Sesión de base de datos
    
    Returns:
        JSONResponse: Mensaje de éxito con ID del usuario o error de autenticación
    
    Raises:
        HTTPException: Si las credenciales son inválidas
    """
    user = db.query(ModelUser).filter(ModelUser.username == username).first()
    if not user or user.password != password:
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")
    else:
        return JSONResponse(
            content={"message": "Login correcto", "id_user": user.id},
            status_code=200
        )


@routerlogin.get("/login/{id}", tags=['login'])
def get_user_id(id: int, db: Session = Depends(get_db)):
    """
    Obtiene la información de un usuario por su ID.
    
    Args:
        id (int): ID del usuario a consultar
        db (Session): Sesión de base de datos
    
    Returns:
        JSONResponse: Datos del usuario si existe, mensaje de error si no
        
    Códigos de respuesta:
        200: Usuario encontrado
        404: Usuario no encontrado
    """
    data = db.query(ModelUser).filter(ModelUser.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={"message": "Recurso no encontrado"})
    else:         
        return JSONResponse(status_code=200, content=jsonable_encoder(data))


@routerlogin.get("/logindatos/{username}", tags=['login'])
def get_user_id(username: str, db: Session = Depends(get_db)):
    """
    Obtiene la información de un usuario por su nombre de usuario.
    
    Args:
        username (str): Nombre de usuario a consultar
        db (Session): Sesión de base de datos
    
    Returns:
        JSONResponse: Datos del usuario si existe, mensaje de error si no
        
    Códigos de respuesta:
        200: Usuario encontrado
        404: Usuario no encontrado
    """
    data = db.query(ModelUser).filter(ModelUser.username == username).first()
    if not data:
        return JSONResponse(status_code=404, content={"message": "Recurso no encontrado"})
    else:         
        return JSONResponse(status_code=200, content=jsonable_encoder(data))