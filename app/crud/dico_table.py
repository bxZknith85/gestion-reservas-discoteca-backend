from sqlalchemy.orm import Session

from app.models.core import DicoTable
from app.schemas.table import DicoTableCreate, DicoTableUpdate


class CRUDDicoTable:
    @staticmethod
    def crear(db: Session, mesa: DicoTableCreate) -> DicoTable:
        db_mesa = DicoTable(**mesa.model_dump())
        db.add(db_mesa)
        db.commit()
        db.refresh(db_mesa)
        return db_mesa

    @staticmethod
    def obtener_por_id(db: Session, table_id: int) -> DicoTable:
        return db.query(DicoTable).filter(DicoTable.id == table_id).first()

    @staticmethod
    def obtener_por_numero(db: Session, number: int) -> DicoTable:
        return db.query(DicoTable).filter(DicoTable.number == number).first()

    @staticmethod
    def obtener_todas(db: Session, skip: int = 0, limit: int = 100) -> list[DicoTable]:
        return db.query(DicoTable).offset(skip).limit(limit).all()

    @staticmethod
    def actualizar(db: Session, table_id: int, mesa_update: DicoTableUpdate) -> DicoTable:
        db_mesa = CRUDDicoTable.obtener_por_id(db, table_id)
        if db_mesa:
            update_data = mesa_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_mesa, key, value)
            db.add(db_mesa)
            db.commit()
            db.refresh(db_mesa)
        return db_mesa

    @staticmethod
    def eliminar(db: Session, table_id: int) -> bool:
        db_mesa = CRUDDicoTable.obtener_por_id(db, table_id)
        if db_mesa:
            db.delete(db_mesa)
            db.commit()
            return True
        return False
