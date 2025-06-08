from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import date

Base = declarative_base()

class Asignacion(Base):
    __tablename__ = "asignaciones"
    id_asignacion = Column(Integer, primary_key=True, index=True)
    id_equipo = Column(Integer, ForeignKey("equipos.id_equipo"))
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date)

def create_or_update_asignacion(db: Session, id_equipo: int, id_usuario: int):
    # Busca asignación activa para ese equipo
    asignacion = db.query(Asignacion).filter_by(id_equipo=id_equipo, fecha_fin=None).first()
    if asignacion:
        # Actualiza usuario asignado
        asignacion.id_usuario = id_usuario
        asignacion.fecha_inicio = date.today()
    else:
        # Crea nueva asignación
        nueva = Asignacion(
            id_equipo=id_equipo,
            id_usuario=id_usuario,
            fecha_inicio=date.today()
        )
        db.add(nueva)
    db.commit()