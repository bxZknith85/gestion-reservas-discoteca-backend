"""Endpoints para gestión de reservas"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.endpoints.auth import get_current_user
from app.crud import reservation as crud_reservation
from app.db.database import get_db
from app.schemas.reservation import (
    ReservationCreate,
    ReservationResponse,
    ReservationUpdate,
)
from app.schemas.usuario import UsuarioResponse

router = APIRouter(prefix="/reservations", tags=["reservations"])


@router.post("/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
def crear_reserva(
    reserva: ReservationCreate, db: Session = Depends(get_db), _usuario: UsuarioResponse = Depends(get_current_user)
):
    """Crear una nueva reserva"""
    return crud_reservation.crear(db, reserva)


@router.get("/{reservation_id}", response_model=ReservationResponse)
def obtener_reserva(
    reservation_id: int, db: Session = Depends(get_db), _usuario: UsuarioResponse = Depends(get_current_user)
):
    """Obtener una reserva por ID"""
    reserva = crud_reservation.obtener_por_id(db, reservation_id)
    if not reserva:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada")
    return reserva


@router.get("/user/{user_id}", response_model=list[ReservationResponse])
def listar_reservas_usuario(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _usuario: UsuarioResponse = Depends(get_current_user),
):
    """Listar reservas de un usuario específico"""
    return crud_reservation.obtener_por_usuario(db, user_id, skip, limit)


@router.get("/", response_model=list[ReservationResponse])
def listar_reservas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _usuario: UsuarioResponse = Depends(get_current_user),
):
    """Listar todas las reservas"""
    return crud_reservation.obtener_todas(db, skip, limit)


@router.put("/{reservation_id}", response_model=ReservationResponse)
def actualizar_reserva(
    reservation_id: int,
    reserva_update: ReservationUpdate,
    db: Session = Depends(get_db),
    _usuario: UsuarioResponse = Depends(get_current_user),
):
    """Actualizar una reserva"""
    reserva = crud_reservation.actualizar(db, reservation_id, reserva_update)
    if not reserva:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada")
    return reserva


@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_reserva(
    reservation_id: int, db: Session = Depends(get_db), _usuario: UsuarioResponse = Depends(get_current_user)
):
    """Eliminar una reserva"""
    if not crud_reservation.eliminar(db, reservation_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada")
