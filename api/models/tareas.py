"""
Módulo que define el modelo de tareas en el sistema.
Este modelo gestiona la información de las tareas, incluyendo su programación,
ubicación, requisitos de voluntarios y asignaciones.
"""

from sqlalchemy import Column, ForeignKey, String, Integer, Boolean
from sqlalchemy.orm import relationship
from ..database import Base


class Tareas(Base):
    """
    Clase que representa la tabla de tareas en el sistema.
    
    Esta tabla almacena toda la información relacionada con las tareas,
    incluyendo detalles temporales y la gestión de voluntarios
    y coordinadores asignados.
    """
    
    __tablename__ = "tareas"  # Nombre de la tabla en la base de datos

    # Identificadores y relaciones
    id = Column(Integer, primary_key=True, index=True)  # Identificador único de la tarea
    user_id = Column(Integer, ForeignKey('users.id'))   # Usuario que creó la tarea
    
    # Información básica de la tarea
    tarea_name = Column(String, nullable=False)        # Nombre o descripción de la tarea
    tarea_ubicacion = Column(String, nullable=False)   # Ubicación donde se realizará la tarea
    
    # Programación temporal
    year = Column(Integer, nullable=False)   # Año de realización
    month = Column(Integer, nullable=False)  # Mes de realización
    day = Column(Integer, nullable=False)    # Día de realización
    turno = Column(String, nullable=False)   # Turno asignado para la tarea
    
    # Gestión de voluntarios
    voluntarios_necesarios = Column(Integer, nullable=False)  # Número total de voluntarios requeridos
    voluntarios_asignados = Column(Integer)                  # Número actual de voluntarios asignados
    
    # IDs de voluntarios asignados (hasta 5 voluntarios)
    id_voluntario_Asignado_1 = Column(String)  # ID del primer voluntario
    id_voluntario_Asignado_2 = Column(String)  # ID del segundo voluntario
    id_voluntario_Asignado_3 = Column(String)  # ID del tercer voluntario
    id_voluntario_Asignado_4 = Column(String)  # ID del cuarto voluntario
    id_voluntario_Asignado_5 = Column(String)  # ID del quinto voluntario
    
    # Gestión de coordinación
    coordinador = Column(Boolean, default=False)           # Indica si la tarea requiere coordinador
    coordinador_Asignado = Column(Boolean, default=False)  # Indica si ya se asignó un coordinador