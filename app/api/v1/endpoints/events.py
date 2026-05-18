"""Endpoints para gestión de eventos"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.endpoints.auth import get_current_user
from app.crud import event as crud_event
from app.db.database import get_db
from app.schemas.event import EventCreate, EventResponse, EventUpdate
from app.schemas.usuario import UsuarioResponse

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def crear_evento(
    evento: EventCreate, db: Session = Depends(get_db), _usuario: UsuarioResponse = Depends(get_current_user)
):
    """Crear un nuevo evento"""
    return crud_event.crear(db, evento)


@router.get("/{event_id}", response_model=EventResponse)
def obtener_evento(event_id: int, db: Session = Depends(get_db)):
    """Obtener un evento por ID"""
    evento = crud_event.obtener_por_id(db, event_id)
    if not evento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento no encontrado")
    return evento


@router.get("/", response_model=list[EventResponse])
def listar_eventos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar todos los eventos"""
    return crud_event.obtener_todos(db, skip, limit)


@router.put("/{event_id}", response_model=EventResponse)
def actualizar_evento(
    event_id: int,
    evento_update: EventUpdate,
    db: Session = Depends(get_db),
    _usuario: UsuarioResponse = Depends(get_current_user),
):
    """Actualizar un evento"""
    evento = crud_event.actualizar(db, event_id, evento_update)
    if not evento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento no encontrado")
    return evento


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_evento(
    event_id: int, db: Session = Depends(get_db), _usuario: UsuarioResponse = Depends(get_current_user)
):
    """Eliminar un evento"""
    if not crud_event.eliminar(db, event_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento no encontrado")
