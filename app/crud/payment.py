from sqlalchemy.orm import Session

from app.models.transactions import Payment
from app.schemas.payment import PaymentCreate, PaymentUpdate


class CRUDPayment:
    @staticmethod
    def crear(db: Session, obj: PaymentCreate) -> Payment:
        db_obj = Payment(**obj.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def obtener_por_id(db: Session, id: int) -> Payment:
        return db.query(Payment).filter(Payment.id == id).first()

    @staticmethod
    def obtener_por_orden(db: Session, order_id: int) -> list[Payment]:
        return db.query(Payment).filter(Payment.order_id == order_id).all()

    @staticmethod
    def obtener_pendientes(db: Session, skip: int = 0, limit: int = 100) -> list[Payment]:
        return db.query(Payment).filter(Payment.status == "pending").offset(skip).limit(limit).all()

    @staticmethod
    def obtener_todos(db: Session, skip: int = 0, limit: int = 100) -> list[Payment]:
        return db.query(Payment).offset(skip).limit(limit).all()

    @staticmethod
    def actualizar(db: Session, id: int, obj_update: PaymentUpdate) -> Payment:
        db_obj = CRUDPayment.obtener_por_id(db, id)
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
        db_obj = CRUDPayment.obtener_por_id(db, id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
            return True
        return False
