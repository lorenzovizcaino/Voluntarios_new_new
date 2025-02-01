"""
Módulo que define la tabla de relación entre tareas y usuarios.
Este modelo gestiona la asignación de tareas a usuarios específicos en el sistema.
"""

from sqlalchemy import Column, ForeignKey, String, Integer, Boolean
from sqlalchemy.orm import relationship
from ..database import Base


class TareasAsignadas(Base):
    """
    Clase que representa la tabla de asignación de tareas a usuarios.
    
    Esta tabla actúa como una relación many-to-many entre las tablas
    'tareas' y 'users', permitiendo asignar múltiples tareas a múltiples usuarios
    y viceversa.
    """
    
    __tablename__ = "tareas_asignadas"  # Nombre de la tabla en la base de datos
    
    # Identificador único para cada asignación
    id = Column(Integer, primary_key=True, index=True)
    
    # Relaciones con otras tablas
    tarea_id = Column(Integer, ForeignKey('tareas.id'))  # ID de la tarea asignada
    user_id = Column(Integer, ForeignKey('users.id'))    # ID del usuario al que se asigna la tarea