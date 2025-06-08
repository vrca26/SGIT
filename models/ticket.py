from database import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Session


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

def create_ticket(db: Session, ticket: Ticket):
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket   

def update_ticket(db: Session, ticket_id: int, updates: dict):
    ticket = db.query(Ticket).filter(Ticket.id_ticket == ticket_id).first()
    if not ticket:
        return None
    for key, value in updates.items():
        setattr(ticket, key, value)
    db.commit()
    db.refresh(ticket)
    return ticket

def delete_ticket(db: Session, ticket_id: int):
    ticket = db.query(Ticket).filter(Ticket.id_ticket == ticket_id).first()
    if not ticket:
        return None
    db.delete(ticket)
    db.commit()
    return ticket