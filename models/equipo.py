from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Session
from database import Base


class Equipo(Base):
    __tablename__ = "equipos"
    id_equipo = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(50), nullable=False)
    marca = Column(String(50))
    modelo = Column(String(50))
    serie = Column(String(100))
    estado = Column(String(20), default="disponible")
    proveedor_id = Column(Integer, ForeignKey("proveedores.id_proveedor"))

def get_all_equipos(db: Session):
    return db.query(Equipo).all()

def get_equipo_by_id(db: Session, id_equipo: int):
    return db.query(Equipo).filter_by(id_equipo=id_equipo).first()

def create_equipo(db: Session, tipo, marca, modelo, serie, estado, proveedor_id, id_usuario):
    nuevo = Equipo(
        tipo=tipo,
        marca=marca,
        modelo=modelo,
        serie=serie,
        estado=estado,
        proveedor_id=proveedor_id
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    if id_usuario:
        from .asignacion import create_asignacion
        from datetime import date
        create_asignacion(db, id_usuario, nuevo.id_equipo, fecha_inicio=date.today())
    return nuevo

def update_equipo(db: Session, id_equipo, tipo, marca, modelo, serie, estado, proveedor_id, id_usuario):
    equipo = get_equipo_by_id(db, id_equipo)
    if not equipo:
        return "Equipo no encontrado."
    equipo.tipo = tipo
    equipo.marca = marca
    equipo.modelo = modelo
    equipo.serie = serie
    equipo.estado = estado
    equipo.proveedor_id = proveedor_id
    db.commit()
    if id_usuario:
        from .asignacion import create_asignacion
        from datetime import date
        create_asignacion(db, id_usuario, equipo.id_equipo, fecha_inicio=date.today())
    return None

def delete_equipo(db: Session, id_equipo: int):
    equipo = get_equipo_by_id(db, id_equipo)
    if not equipo:
        return "Equipo no encontrado."
    # Elimina la validación de asignaciones y tickets relacionados
    db.delete(equipo)
    db.commit()
    return None