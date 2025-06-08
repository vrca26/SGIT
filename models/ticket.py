from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from database import Base
from sqlalchemy.sql import func

class Ticket(Base):
    __tablename__ = "tickets"
    id_ticket = Column(Integer, primary_key=True, index=True)
    id_equipo = Column(Integer, ForeignKey("equipos.id_equipo"))
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    asunto = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=False)
    estado = Column(String(20))
    fecha_creacion = Column(DateTime(timezone=False), server_default=func.now())