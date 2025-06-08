from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()

class Proveedor(Base):
    __tablename__ = "proveedores"
    id_proveedor = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    contacto = Column(String(100))
    telefono = Column(String(20))

def get_all_proveedores(db: Session):
    return db.query(Proveedor).all()

def get_proveedor_by_id(db: Session, id_proveedor: int):
    return db.query(Proveedor).filter_by(id_proveedor=id_proveedor).first()

def create_proveedor(db: Session, nombre: str, contacto: str, telefono: str):
    nuevo = Proveedor(nombre=nombre, contacto=contacto, telefono=telefono)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def update_proveedor(db: Session, id_proveedor: int, nombre: str, contacto: str, telefono: str):
    proveedor = get_proveedor_by_id(db, id_proveedor)
    if not proveedor:
        return "Proveedor no encontrado."
    proveedor.nombre = nombre
    proveedor.contacto = contacto
    proveedor.telefono = telefono
    db.commit()
    return None

def delete_proveedor(db: Session, id_proveedor: int):
    proveedor = get_proveedor_by_id(db, id_proveedor)
    if proveedor:
        db.delete(proveedor)
        db.commit()