from sqlalchemy.orm import Session
from app.models.transactions import Order
from app.schemas.order import OrderCreate, OrderUpdate


class CRUDOrder:
    @staticmethod
    def crear(db: Session, obj: OrderCreate) -> Order:
        db_obj = Order(**obj.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def obtener_por_id(db: Session, id: int) -> Order:
        return db.query(Order).filter(Order.id == id).first()

    @staticmethod
    def obtener_por_usuario(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[Order]:
        return db.query(Order).filter(Order.user_id == user_id).offset(skip).limit(limit).all()

    @staticmethod
    def obtener_todos(db: Session, skip: int = 0, limit: int = 100) -> list[Order]:
        return db.query(Order).offset(skip).limit(limit).all()

    @staticmethod
    def actualizar(db: Session, id: int, obj_update: OrderUpdate) -> Order:
        db_obj = CRUDOrder.obtener_por_id(db, id)
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
        db_obj = CRUDOrder.obtener_por_id(db, id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
            return True
        return False
