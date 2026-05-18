from sqlalchemy.orm import Session

from app.models.core import Event
from app.schemas.event import EventCreate, EventUpdate


class CRUDEvent:
    @staticmethod
    def crear(db: Session, evento: EventCreate) -> Event:
        db_evento = Event(**evento.model_dump())
        db.add(db_evento)
        db.commit()
        db.refresh(db_evento)
        return db_evento

    @staticmethod
    def obtener_por_id(db: Session, event_id: int) -> Event:
        return db.query(Event).filter(Event.id == event_id).first()

    @staticmethod
    def obtener_todos(db: Session, skip: int = 0, limit: int = 100) -> list[Event]:
        return db.query(Event).offset(skip).limit(limit).all()

    @staticmethod
    def actualizar(db: Session, event_id: int, evento_update: EventUpdate) -> Event:
        db_evento = CRUDEvent.obtener_por_id(db, event_id)
        if db_evento:
            update_data = evento_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_evento, key, value)
            db.add(db_evento)
            db.commit()
            db.refresh(db_evento)
        return db_evento

    @staticmethod
    def eliminar(db: Session, event_id: int) -> bool:
        db_evento = CRUDEvent.obtener_por_id(db, event_id)
        if db_evento:
            db.delete(db_evento)
            db.commit()
            return True
        return False
