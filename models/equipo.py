from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Equipo(Base):
    __tablename__ = "equipos"
    id_equipo = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(50), nullable=False)
    marca = Column(String(50))
    modelo = Column(String(50))
    serie = Column(String(100), unique=True)
    estado = Column(String(20))
    proveedor_id = Column(Integer, ForeignKey("proveedores.id_proveedor"))