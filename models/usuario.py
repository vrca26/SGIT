from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

class Usuario(Base):
    __tablename__ = "usuarios"
    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    contraseña = Column(String(255), nullable=False)
    rol = Column(String(20), nullable=False)

def get_all_users(db: Session):
    return db.query(Usuario).all()