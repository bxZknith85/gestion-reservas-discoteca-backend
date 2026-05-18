from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.reserva import CRUDReserva
from app.db.database import get_db
from app.schemas.reserva import ReservaCreate, ReservaResponse, ReservaUpdate

router = APIRouter(prefix="/reservas", tags=["reservas"])


@router.post("/", response_model=ReservaResponse)
def crear_reserva(reserva: ReservaCreate, db: Session = Depends(get_db)):
    """Crear una nueva reserva"""
    return CRUDReserva.crear(db, reserva)


@router.get("/{reserva_id}", response_model=ReservaResponse)
def obtener_reserva(reserva_id: int, db: Session = Depends(get_db)):
    """Obtener una reserva por ID"""
    reserva = CRUDReserva.obtener_por_id(db, reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva


@router.get("/", response_model=list[ReservaResponse])
def listar_reservas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar todas las reservas"""
    return CRUDReserva.obtener_todas(db, skip, limit)


@router.get("/usuario/{usuario_id}", response_model=list[ReservaResponse])
def listar_reservas_usuario(usuario_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar reservas de un usuario específico"""
    return CRUDReserva.obtener_por_usuario(db, usuario_id, skip, limit)


@router.put("/{reserva_id}", response_model=ReservaResponse)
def actualizar_reserva(reserva_id: int, reserva_update: ReservaUpdate, db: Session = Depends(get_db)):
    """Actualizar una reserva"""
    reserva = CRUDReserva.actualizar(db, reserva_id, reserva_update)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva


@router.delete("/{reserva_id}")
def eliminar_reserva(reserva_id: int, db: Session = Depends(get_db)):
    """Eliminar una reserva"""
    if not CRUDReserva.eliminar(db, reserva_id):
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return {"message": "Reserva eliminada exitosamente"}
