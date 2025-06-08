from database import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from database import Base


class Ticket(Base):
    __tablename__ = "tickets"
    id_ticket = Column(Integer, primary_key=True, index=True)
    id_equipo = Column(Integer, ForeignKey("equipos.id_equipo"))
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"))
    asunto = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=False)
    estado = Column(String(20))
    fecha_creacion = Column(DateTime(timezone=False), server_default=func.now())

def get_recent_tickets(db: Session, limit=10):
    return db.query(Ticket).order_by(Ticket.id_ticket.desc()).limit(limit).all()

def get_ticket_stats(db: Session):
    abiertos = db.query(Ticket).filter_by(estado="abierto").count()
    en_proceso = db.query(Ticket).filter_by(estado="en proceso").count()
    cerrados = db.query(Ticket).filter_by(estado="cerrado").count()
    return {"abiertos": abiertos, "en_proceso": en_proceso, "cerrados": cerrados}