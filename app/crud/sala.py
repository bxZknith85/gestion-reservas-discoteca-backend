from sqlalchemy.orm import Session

from app.models.usuario import Sala
from app.schemas.sala import SalaCreate, SalaUpdate


class CRUDSala:
    @staticmethod
    def crear(db: Session, sala: SalaCreate) -> Sala:
        db_sala = Sala(**sala.model_dump())
        db.add(db_sala)
        db.commit()
        db.refresh(db_sala)
        return db_sala

    @staticmethod
    def obtener_por_id(db: Session, sala_id: int) -> Sala:
        return db.query(Sala).filter(Sala.id == sala_id).first()

    @staticmethod
    def obtener_todas(db: Session, skip: int = 0, limit: int = 100) -> list[Sala]:
        return db.query(Sala).offset(skip).limit(limit).all()

    @staticmethod
    def actualizar(db: Session, sala_id: int, sala_update: SalaUpdate) -> Sala:
        db_sala = CRUDSala.obtener_por_id(db, sala_id)
        if db_sala:
            update_data = sala_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_sala, key, value)
            db.add(db_sala)
            db.commit()
            db.refresh(db_sala)
        return db_sala

    @staticmethod
    def eliminar(db: Session, sala_id: int) -> bool:
        db_sala = CRUDSala.obtener_por_id(db, sala_id)
        if db_sala:
            db.delete(db_sala)
            db.commit()
            return True
        return False
