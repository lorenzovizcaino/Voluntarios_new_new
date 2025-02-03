"""
Módulo que define los modelos Pydantic utilizados para la validación
de datos en las peticiones a la API. Estos modelos aseguran que los datos
recibidos cumplan con la estructura y tipos esperados.
"""

from pydantic import BaseModel
from typing import Optional


class LoginRequest(BaseModel):
    """
    Modelo Pydantic para validar las peticiones de login.
    
    Este modelo define la estructura esperada para las credenciales
    de autenticación en la API.
    
    Attributes:
        username (str): Nombre de usuario para la autenticación
        password (str): Contraseña del usuario
        
    Example:
        {
            "username": "usuario123",
            "password": "contraseña123"
        }
    """
    username: str  # Nombre de usuario requerido
    password: str  # Contraseña requerida

