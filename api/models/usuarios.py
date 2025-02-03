"""
Módulo que define el modelo principal de usuarios en el sistema.
Este modelo gestiona la información básica de autenticación y tipo de usuario
para el control de acceso al sistema.
"""

from sqlalchemy import Column, String, Integer
from ..database import Base


class User(Base):
    """
    Clase que representa la tabla principal de usuarios del sistema.
    
    Esta tabla almacena la información esencial de los usuarios incluyendo
    credenciales de acceso y su rol en el sistema. Es la tabla base que se
    relaciona con otros modelos para extender la información del usuario.
    """
    
    __tablename__ = "users"  # Nombre de la tabla en la base de datos
    
    # Campos de identificación
    id = Column(Integer, primary_key=True, index=True)  # Identificador único del usuario
    
    # Credenciales de acceso
    username = Column(String, unique=True, index=True)  # Nombre de usuario único
    password = Column(String)                          # Contraseña del usuario 
    
    # Información de rol
    tipo_usuario = Column(String)  # Tipo o rol del usuario en el sistema
