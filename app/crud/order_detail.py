from sqlalchemy.orm import Session
from app.models.transactions import OrderDetail
from app.schemas.order_detail import OrderDetailCreate, OrderDetailUpdate


class CRUDOrderDetail:
    @staticmethod
    def crear(db: Session, obj: OrderDetailCreate) -> OrderDetail:
        db_obj = OrderDetail(**obj.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def obtener_por_id(db: Session, id: int) -> OrderDetail:
        return db.query(OrderDetail).filter(OrderDetail.id == id).first()

    @staticmethod
    def obtener_por_orden(db: Session, order_id: int) -> list[OrderDetail]:
        return db.query(OrderDetail).filter(OrderDetail.order_id == order_id).all()

    @staticmethod
    def obtener_todos(db: Session, skip: int = 0, limit: int = 100) -> list[OrderDetail]:
        return db.query(OrderDetail).offset(skip).limit(limit).all()

    @staticmethod
    def actualizar(db: Session, id: int, obj_update: OrderDetailUpdate) -> OrderDetail:
        db_obj = CRUDOrderDetail.obtener_por_id(db, id)
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
        db_obj = CRUDOrderDetail.obtener_por_id(db, id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
            return True
        return False
