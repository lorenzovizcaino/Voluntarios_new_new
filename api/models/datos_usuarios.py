from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from ..database import Base

class DatosUser(Base):
    __tablename__ = "datos_users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    email = Column(String)
    direccion=Column(String)
    telefono=Column(String)
    tipo_usuario = Column(String)
    config = Column(Boolean, default=False)
    coordinador=Column(Boolean, default=False)
    amigo=Column(String)
