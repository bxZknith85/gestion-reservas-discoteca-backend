from sqlalchemy.orm import Session
from app.models.core import TablePrice
from app.schemas.table_price import TablePriceCreate, TablePriceUpdate


class CRUDTablePrice:
    @staticmethod
    def crear(db: Session, obj: TablePriceCreate) -> TablePrice:
        db_obj = TablePrice(**obj.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def obtener_por_id(db: Session, id: int) -> TablePrice:
        return db.query(TablePrice).filter(TablePrice.id == id).first()

    @staticmethod
    def obtener_por_evento(db: Session, event_id: int) -> list[TablePrice]:
        return db.query(TablePrice).filter(TablePrice.event_id == event_id).all()

    @staticmethod
    def obtener_por_mesa(db: Session, table_id: int) -> list[TablePrice]:
        return db.query(TablePrice).filter(TablePrice.table_id == table_id).all()

    @staticmethod
    def obtener_todos(db: Session, skip: int = 0, limit: int = 100) -> list[TablePrice]:
        return db.query(TablePrice).offset(skip).limit(limit).all()

    @staticmethod
    def actualizar(db: Session, id: int, obj_update: TablePriceUpdate) -> TablePrice:
        db_obj = CRUDTablePrice.obtener_por_id(db, id)
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
        db_obj = CRUDTablePrice.obtener_por_id(db, id)
        if db_obj:
            db.delete(db_obj)
            db.commit()
            return True
        return False
