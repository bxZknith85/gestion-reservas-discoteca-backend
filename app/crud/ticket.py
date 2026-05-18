from sqlalchemy.orm import Session

from app.models.transactions import Ticket
from app.schemas.ticket import TicketCreate, TicketUpdate


class CRUDTicket:
    @staticmethod
    def crear(db: Session, ticket: TicketCreate) -> Ticket:
        db_ticket = Ticket(**ticket.model_dump())
        db.add(db_ticket)
        db.commit()
        db.refresh(db_ticket)
        return db_ticket

    @staticmethod
    def obtener_por_id(db: Session, ticket_id: int) -> Ticket:
        return db.query(Ticket).filter(Ticket.id == ticket_id).first()

    @staticmethod
    def obtener_por_usuario(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[Ticket]:
        return db.query(Ticket).filter(Ticket.user_id == user_id).offset(skip).limit(limit).all()

    @staticmethod
    def obtener_todos(db: Session, skip: int = 0, limit: int = 100) -> list[Ticket]:
        return db.query(Ticket).offset(skip).limit(limit).all()

    @staticmethod
    def actualizar(db: Session, ticket_id: int, ticket_update: TicketUpdate) -> Ticket:
        db_ticket = CRUDTicket.obtener_por_id(db, ticket_id)
        if db_ticket:
            update_data = ticket_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_ticket, key, value)
            db.add(db_ticket)
            db.commit()
            db.refresh(db_ticket)
        return db_ticket

    @staticmethod
    def eliminar(db: Session, ticket_id: int) -> bool:
        db_ticket = CRUDTicket.obtener_por_id(db, ticket_id)
        if db_ticket:
            db.delete(db_ticket)
            db.commit()
            return True
        return False
