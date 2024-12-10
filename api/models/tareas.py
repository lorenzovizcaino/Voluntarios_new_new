from sqlalchemy import Column, ForeignKey, String, Integer, Boolean
from sqlalchemy.orm import relationship
from ..database import Base

class Tareas(Base):
    __tablename__ = "tareas"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    tarea_name = Column(String, nullable=False)
    tarea_ubicacion = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    day = Column(Integer, nullable=False)    
    turno = Column(String, nullable=False)
    voluntarios_necesarios = Column(Integer, nullable=False)
    voluntarios_asignados = Column(Integer)
    id_voluntario_Asignado_1 = Column(String)
    id_voluntario_Asignado_2 = Column(String)
    id_voluntario_Asignado_3 = Column(String)
    id_voluntario_Asignado_4 = Column(String)
    id_voluntario_Asignado_5 = Column(String)
    coordinador = Column(Boolean, default=False)    
    coordinador_Asignado = Column(Boolean, default=False)
