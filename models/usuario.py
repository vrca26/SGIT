from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"
    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    contraseña = Column(String(255), nullable=False)
    rol = Column(String(20), nullable=False)

def get_all_users(db: Session):
    return db.query(Usuario).all()

def get_user_by_id(db: Session, id_usuario: int):
    return db.query(Usuario).filter_by(id_usuario=id_usuario).first()

def create_user(db: Session, nombre: str, correo: str, contraseña: str, rol: str):
    if db.query(Usuario).filter_by(correo=correo).first():
        return None, "Correo ya registrado."
    nuevo = Usuario(nombre=nombre, correo=correo, contraseña=contraseña, rol=rol)
    db.add(nuevo)
    try:
        db.commit()
        db.refresh(nuevo)
        return nuevo, None
    except IntegrityError:
        db.rollback()
        return None, "Error de integridad al crear usuario."
    except Exception as e:
        db.rollback()
        return None, str(e)

def update_user(db: Session, id_usuario: int, nombre: str, correo: str, contraseña: str, rol: str):
    usuario = db.query(Usuario).filter_by(id_usuario=id_usuario).first()
    if not usuario:
        return "Usuario no encontrado."
    usuario.nombre = nombre
    usuario.correo = correo
    if contraseña:
        usuario.contraseña = contraseña
    usuario.rol = rol
    try:
        db.commit()
        return None
    except IntegrityError:
        db.rollback()
        return "Error de integridad al actualizar usuario."
    except Exception as e:
        db.rollback()
        return str(e)

def delete_user(db: Session, id_usuario: int):
    usuario = db.query(Usuario).filter_by(id_usuario=id_usuario).first()
    if usuario:
        db.delete(usuario)
        db.commit()