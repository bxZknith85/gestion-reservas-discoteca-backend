from sqlalchemy.orm import Session

from app.models.usuario import Evento
from app.schemas.evento import EventoCreate, EventoUpdate


class CRUDEvento:
    @staticmethod
    def crear(db: Session, evento: EventoCreate) -> Evento:
        db_evento = Evento(**evento.model_dump())
        db.add(db_evento)
        db.commit()
        db.refresh(db_evento)
        return db_evento

    @staticmethod
    def obtener_por_id(db: Session, evento_id: int) -> Evento:
        return db.query(Evento).filter(Evento.id == evento_id).first()

    @staticmethod
    def obtener_todos(db: Session, skip: int = 0, limit: int = 100) -> list[Evento]:
        return db.query(Evento).offset(skip).limit(limit).all()

    @staticmethod
    def actualizar(db: Session, evento_id: int, evento_update: EventoUpdate) -> Evento:
        db_evento = CRUDEvento.obtener_por_id(db, evento_id)
        if db_evento:
            update_data = evento_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_evento, key, value)
            db.add(db_evento)
            db.commit()
            db.refresh(db_evento)
        return db_evento

    @staticmethod
    def eliminar(db: Session, evento_id: int) -> bool:
        db_evento = CRUDEvento.obtener_por_id(db, evento_id)
        if db_evento:
            db.delete(db_evento)
            db.commit()
            return True
        return False
