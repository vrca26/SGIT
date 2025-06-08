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
            "fecha_fin": a.Asignacion.fecha_fin,
            "id_usuario": a.Asignacion.id_usuario,
            "id_equipo": a.Asignacion.id_equipo,
        }
        for a in results
    ]

def get_all_asignaciones(db: Session):
    return db.query(Asignacion).all()

def get_asignacion_by_id(db: Session, id_asignacion: int):
    return db.query(Asignacion).filter_by(id_asignacion=id_asignacion).first()

def create_asignacion(db: Session, id_usuario: int, id_equipo: int, fecha_inicio, fecha_fin=None):
    nueva = Asignacion(
        id_usuario=id_usuario,
        id_equipo=id_equipo,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def update_asignacion(db: Session, id_asignacion: int, id_usuario: int, id_equipo: int, fecha_inicio, fecha_fin=None):
    asignacion = get_asignacion_by_id(db, id_asignacion)
    if not asignacion:
        return "Asignación no encontrada."
    asignacion.id_usuario = id_usuario
    asignacion.id_equipo = id_equipo
    asignacion.fecha_inicio = fecha_inicio
    asignacion.fecha_fin = fecha_fin
    db.commit()
    return None

def delete_asignacion(db: Session, id_asignacion: int):
    asignacion = get_asignacion_by_id(db, id_asignacion)
    if asignacion:
        db.delete(asignacion)
        db.commit()