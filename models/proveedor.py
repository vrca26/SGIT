from sqlalchemy import Column, Integer, String
from database import Base

class Proveedor(Base):
    __tablename__ = "proveedores"
    
    id_proveedor = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    contacto = Column(String(100))
    telefono = Column(String(20))