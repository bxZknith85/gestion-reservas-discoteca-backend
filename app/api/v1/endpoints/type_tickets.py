from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.endpoints.auth import get_current_user
from app.crud import type_ticket as crud_type_ticket
from app.db.database import get_db
from app.schemas.type_ticket import (
    TypeTicketCreate,
    TypeTicketResponse,
    TypeTicketUpdate,
)
from app.schemas.usuario import UsuarioResponse

router = APIRouter(prefix="/type-tickets", tags=["type-tickets"])


@router.post("/", response_model=TypeTicketResponse, status_code=status.HTTP_201_CREATED)
def crear(obj: TypeTicketCreate, db: Session = Depends(get_db), _usuario: UsuarioResponse = Depends(get_current_user)):
    return crud_type_ticket.crear(db, obj)


@router.get("/{id}", response_model=TypeTicketResponse)
def obtener(id: int, db: Session = Depends(get_db), _usuario: UsuarioResponse = Depends(get_current_user)):
    obj = crud_type_ticket.obtener_por_id(db, id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo de ticket no encontrado")
    return obj


@router.get("/event/{event_id}", response_model=list[TypeTicketResponse])
def listar_por_evento(
    event_id: int, db: Session = Depends(get_db), _usuario: UsuarioResponse = Depends(get_current_user)
):
    return crud_type_ticket.obtener_por_evento(db, event_id)


@router.get("/", response_model=list[TypeTicketResponse])
def listar(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _usuario: UsuarioResponse = Depends(get_current_user),
):
    return crud_type_ticket.obtener_todos(db, skip, limit)


@router.put("/{id}", response_model=TypeTicketResponse)
def actualizar(
    id: int,
    obj_update: TypeTicketUpdate,
    db: Session = Depends(get_db),
    _usuario: UsuarioResponse = Depends(get_current_user),
):
    obj = crud_type_ticket.actualizar(db, id, obj_update)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo de ticket no encontrado")
    return obj


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(id: int, db: Session = Depends(get_db), _usuario: UsuarioResponse = Depends(get_current_user)):
    if not crud_type_ticket.eliminar(db, id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tipo de ticket no encontrado")
