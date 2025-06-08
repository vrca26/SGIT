from database import Base
from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import Session
from .usuario import Usuario
from .equipo import Equipo

class Asignacion(Base):
    __tablename__ = "asignaciones"
    id_asignacion = Column(Integer, primary_key=True, index=True)
    id_equipo = Column(Integer, ForeignKey("equipos.id_equipo"))
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date)

def get_recent_assignments(db: Session, limit=10):
    # Devuelve asignaciones con nombre de usuario y equipo
    results = (
        db.query(Asignacion, Usuario.nombre.label("nombre_usuario"), Equipo.tipo.label("nombre_equipo"))
        .join(Usuario, Asignacion.id_usuario == Usuario.id_usuario)
        .join(Equipo, Asignacion.id_equipo == Equipo.id_equipo)
        .order_by(Asignacion.id_asignacion.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "id_asignacion": a.Asignacion.id_asignacion,
            "nombre_usuario": a.nombre_usuario,
            "nombre_equipo": a.nombre_equipo,
            "fecha_inicio": a.Asignacion.fecha_inicio,
        }
        for a in results
    ]