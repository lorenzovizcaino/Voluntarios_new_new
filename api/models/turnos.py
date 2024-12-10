from sqlalchemy import Column, ForeignKey, String, Integer, Boolean
from sqlalchemy.orm import relationship
from ..database import Base

class Turnos(Base):
    __tablename__ = "turnos"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)    
    turno1 = Column(Boolean, default=False)
    turno2 = Column(Boolean, default=False)
    turno3 = Column(Boolean, default=False)
    turno4 = Column(Boolean, default=False)

    #usuario = relationship("User", back_populates="turnos")

    