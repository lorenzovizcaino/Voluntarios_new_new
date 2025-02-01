"""
Módulo que define el modelo de datos extendido para usuarios en la aplicación.
Utiliza SQLAlchemy como ORM para el mapeo objeto-relacional.
"""

from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from ..database import Base


class DatosUser(Base):
    """
    Clase que representa la tabla de datos extendidos de usuarios.
    
    Esta tabla almacena información adicional relacionada con cada usuario
    del sistema, incluyendo datos de contacto y roles específicos.
    """
    
    __tablename__ = "datos_users"  # Nombre de la tabla en la base de datos

    # Campos de la tabla
    id = Column(Integer, primary_key=True, index=True)  # Identificador único del registro
    user_id = Column(Integer, ForeignKey('users.id'))   # Relación con la tabla principal de usuarios
    
    # Información de contacto
    email = Column(String)      # Correo electrónico del usuario
    direccion = Column(String)  # Dirección física del usuario
    telefono = Column(String)   # Número de teléfono de contacto
    chat_id = Column(String)    # chat_id de Telegram
    
    # Configuración y roles
    tipo_usuario = Column(String)                 # Tipo o categoría del usuario
    config = Column(Boolean, default=False)       # Indica si el usuario ha completado la configuración
    coordinador = Column(Boolean, default=False)  # Indica si el usuario tiene rol de coordinador
    
    # Relaciones
    amigo = Column(String)  # Almacena un usuario, preferido para la realización de las tareas
