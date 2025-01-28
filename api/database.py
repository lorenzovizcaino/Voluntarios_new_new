from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Conexión a la base de datos SQLite
DATABASE_URL = "sqlite:///./frontend/voluntarios.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)

# Función para obtener una sesión de la base de datos
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
