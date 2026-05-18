from sqlalchemy.orm import Session

from app.models.transactions import Reservation
from app.schemas.reservation import ReservationCreate, ReservationUpdate


class CRUDReservation:
    @staticmethod
    def crear(db: Session, reserva: ReservationCreate) -> Reservation:
        db_reserva = Reservation(**reserva.model_dump())
        db.add(db_reserva)
        db.commit()
        db.refresh(db_reserva)
        return db_reserva

    @staticmethod
    def obtener_por_id(db: Session, reservation_id: int) -> Reservation:
        return db.query(Reservation).filter(Reservation.id == reservation_id).first()

    @staticmethod
    def obtener_por_usuario(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[Reservation]:
        return db.query(Reservation).filter(Reservation.user_id == user_id).offset(skip).limit(limit).all()

    @staticmethod
    def obtener_todas(db: Session, skip: int = 0, limit: int = 100) -> list[Reservation]:
        return db.query(Reservation).offset(skip).limit(limit).all()

    @staticmethod
    def actualizar(db: Session, reservation_id: int, reserva_update: ReservationUpdate) -> Reservation:
        db_reserva = CRUDReservation.obtener_por_id(db, reservation_id)
        if db_reserva:
            update_data = reserva_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_reserva, key, value)
            db.add(db_reserva)
            db.commit()
            db.refresh(db_reserva)
        return db_reserva

    @staticmethod
    def eliminar(db: Session, reservation_id: int) -> bool:
        db_reserva = CRUDReservation.obtener_por_id(db, reservation_id)
        if db_reserva:
            db.delete(db_reserva)
            db.commit()
            return True
        return False
