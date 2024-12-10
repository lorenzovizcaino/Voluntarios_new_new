from sqlalchemy import Column, ForeignKey, String, Integer, Boolean
from sqlalchemy.orm import relationship
from ..database import Base

class TareasAsignadas(Base):
    __tablename__ = "tareas_asignadas"
    id = Column(Integer, primary_key=True, index=True)    
    tarea_id = Column(Integer, ForeignKey('tareas.id'))
    user_id = Column(Integer, ForeignKey('users.id'))