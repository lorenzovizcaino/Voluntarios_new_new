"""
Módulo que define los endpoints de la API para gestionar los datos extendidos de usuarios.
Proporciona rutas para consultar y manipular la información adicional de los usuarios
en el sistema.
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
from ..models.datos_usuarios import DatosUser as ModelDatosUser


# Crear instancia del router
routerdatosuser = APIRouter()


class Datos_User(BaseModel):
    """
    Modelo Pydantic que define la estructura de datos para las operaciones
    de la API relacionadas con datos de usuario.
    
    Define los campos requeridos y opcionales para la validación de datos
    en las peticiones HTTP.
    """
    id: Optional[int] = None          # ID opcional para creación/actualización
    user_id: int                      # ID del usuario relacionado
    email: str                        # Correo electrónico
    direccion: str                    # Dirección física
    telefono: str                     # Número de teléfono
    chat_id: str                      # ID de chat para Telegram
    tipo_usuario: str                 # Tipo o rol del usuario
    config: bool                      # Estado de configuración
    coordinador: bool = False         # Indica si es coordinador
    amigo: str                        # Nombre de amigo


@routerdatosuser.get('/datosuser/{id}', tags=['datos_user'])
def get_datos_user(id: int, db: Session = Depends(get_db)):
    """
    Endpoint para obtener los datos extendidos de un usuario específico.
    
    Args:
        id (int): Identificador único del registro de datos de usuario
        db (Session): Sesión de base de datos proporcionada por FastAPI
    
    Returns:
        JSONResponse: Datos del usuario si se encuentra, o mensaje de error si no existe
        
    Códigos de respuesta:
        200: Datos encontrados y devueltos correctamente
        404: No se encontró el registro solicitado
    """
    # Buscar datos del usuario en la base de datos
    data = db.query(ModelDatosUser).filter(ModelDatosUser.id == id).first()
    
    # Retornar respuesta según resultado de la búsqueda
    if not data:
        return JSONResponse(status_code=404, content={"message": "Recurso no encontrado"})
    else:
        return JSONResponse(status_code=200, content=jsonable_encoder(data))