"""
Módulo que define el modelo de turnos en el sistema.
Este modelo gestiona la disponibilidad de los usuarios por turnos
en fechas específicas.
"""

from sqlalchemy import Column, ForeignKey, String, Integer, Boolean
from sqlalchemy.orm import relationship
from ..database import Base


class Turnos(Base):
    """
    Clase que representa la tabla de turnos disponibles por usuario.
    
    Esta tabla almacena la disponibilidad de cada usuario para los diferentes
    turnos en una fecha específica. Cada turno se representa como un valor
    booleano que indica si el usuario está disponible o no.
    """
    
    __tablename__ = "turnos"  # Nombre de la tabla en la base de datos

    # Identificadores y relaciones
    id = Column(Integer, primary_key=True, index=True)  # Identificador único del registro
    user_id = Column(Integer, ForeignKey('users.id'))   # Usuario al que pertenece el turno
    
    # Fecha del turno
    year = Column(Integer)   # Año del turno
    month = Column(Integer)  # Mes del turno
    day = Column(Integer)    # Día del turno
    
    # Disponibilidad por turnos
    turno1 = Column(Boolean, default=False)  # Disponibilidad para el primer turno
    turno2 = Column(Boolean, default=False)  # Disponibilidad para el segundo turno
    turno3 = Column(Boolean, default=False)  # Disponibilidad para el tercer turno
    turno4 = Column(Boolean, default=False)  # Disponibilidad para el cuarto turno

    
    