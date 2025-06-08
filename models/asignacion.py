from sqlalchemy import Column, Integer, Date, ForeignKey
from database import Base

class Asignacion(Base):
    __tablename__ = "asignaciones"
    id_asignacion = Column(Integer, primary_key=True, index=True)
    id_equipo = Column(Integer, ForeignKey("equipos.id_equipo"))
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date)