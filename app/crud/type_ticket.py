from sqlalchemy.orm import Session

from app.models.core import TypeTicket
from app.schemas.type_ticket import TypeTicketCreate, TypeTicketUpdate


class CRUDTypeTicket:
    @staticmethod
    def crear(db: Session, obj: TypeTicketCreate) -> TypeTicket:
        db_obj = TypeTicket(**obj.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def obtener_por_id(db: Session, id: int) -> TypeTicket:
        return db.query(TypeTicket).filter(TypeTicket.id == id).first()

    @staticmethod
    def obtener_por_evento(db: Session, event_id: int) -> list[TypeTicket]:
        return db.query(TypeTicket).filter(TypeTicket.event_id == event_id).all()

    @staticmethod
    def obtener_todos(db: Session, skip: int = 0, limit: int = 100) -> list[TypeTicket]:
        return db.query(TypeTicket).offset(skip).limit(limit).all()

    @staticmethod
    def actualizar(db: Session, id: int, obj_update: TypeTicketUpdate) -> TypeTicket:
        db_obj = CRUDTypeTicket.obtener_por_id(db, id)
        if db_obj:
            update_data = obj_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_obj, key, value)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        return db_obj

    @staticmethod
    def eliminar(db: Session, id: int) -> bool:
        db_obj = CRUDTypeTicket.obtener_por_id(db, id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
            return True
        return False
