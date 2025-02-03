"""
Módulo de configuración y gestión de la base de datos.
Este módulo proporciona la configuración básica de SQLAlchemy, incluyendo
la conexión a la base de datos SQLite y las funciones necesarias para
la gestión de sesiones.
"""

from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexión a la base de datos SQLite
# La base de datos se almacena en el directorio frontend
DATABASE_URL = "sqlite:///./frontend/voluntarios.db"

# Crear el engine de SQLAlchemy con configuración específica para SQLite
# check_same_thread=False permite el acceso desde múltiples hilos
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Configurar la sessionmaker
# autocommit=False: Los cambios deben ser confirmados explícitamente
# autoflush=False: Los cambios no se sincronizan automáticamente con la BD
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para los modelos ORM
Base = declarative_base()


def init_db():
    """
    Inicializa la base de datos creando todas las tablas definidas
    en los modelos que heredan de Base.
    
    Esta función debe ser llamada al inicio de la aplicación para asegurar
    que todas las tablas necesarias existen en la base de datos.
    """
    Base.metadata.create_all(bind=engine)


def get_db():
    """
    Generador de contexto para obtener una sesión de base de datos.    
    
    """
    db = session()
    try:
        yield db
    finally:
        # Asegura que la sesión se cierra incluso si hay errores
        db.close()