from sqlalchemy.orm import Session

from app.models.usuario import Reserva
from app.schemas.reserva import ReservaCreate, ReservaUpdate


class CRUDReserva:
    @staticmethod
    def crear(db: Session, reserva: ReservaCreate) -> Reserva:
        db_reserva = Reserva(**reserva.model_dump())
        db.add(db_reserva)
        db.commit()
        db.refresh(db_reserva)
        return db_reserva

    @staticmethod
    def obtener_por_id(db: Session, reserva_id: int) -> Reserva:
        return db.query(Reserva).filter(Reserva.id == reserva_id).first()

    @staticmethod
    def obtener_por_usuario(db: Session, usuario_id: int, skip: int = 0, limit: int = 100) -> list[Reserva]:
        return db.query(Reserva).filter(Reserva.usuario_id == usuario_id).offset(skip).limit(limit).all()

    @staticmethod
    def obtener_todas(db: Session, skip: int = 0, limit: int = 100) -> list[Reserva]:
        return db.query(Reserva).offset(skip).limit(limit).all()

    @staticmethod
    def actualizar(db: Session, reserva_id: int, reserva_update: ReservaUpdate) -> Reserva:
        db_reserva = CRUDReserva.obtener_por_id(db, reserva_id)
        if db_reserva:
            update_data = reserva_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_reserva, key, value)
            db.add(db_reserva)
            db.commit()
            db.refresh(db_reserva)
        return db_reserva

    @staticmethod
    def eliminar(db: Session, reserva_id: int) -> bool:
        db_reserva = CRUDReserva.obtener_por_id(db, reserva_id)
        if db_reserva:
            db.delete(db_reserva)
            db.commit()
            return True
        return False
