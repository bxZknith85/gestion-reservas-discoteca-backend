from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.endpoints.auth import get_current_user
from app.crud import ticket as crud_ticket
from app.db.database import get_db
from app.schemas.ticket import TicketCreate, TicketResponse, TicketUpdate
from app.schemas.usuario import UsuarioResponse

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def crear_ticket(
    ticket: TicketCreate, db: Session = Depends(get_db), _usuario: UsuarioResponse = Depends(get_current_user)
):
    return crud_ticket.crear(db, ticket)


@router.get("/{ticket_id}", response_model=TicketResponse)
def obtener_ticket(
    ticket_id: int, db: Session = Depends(get_db), _usuario: UsuarioResponse = Depends(get_current_user)
):
    ticket = crud_ticket.obtener_por_id(db, ticket_id)
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket no encontrado")
    return ticket


@router.get("/user/{user_id}", response_model=list[TicketResponse])
def listar_tickets_usuario(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _usuario: UsuarioResponse = Depends(get_current_user),
):
    return crud_ticket.obtener_por_usuario(db, user_id, skip, limit)


@router.get("/", response_model=list[TicketResponse])
def listar_tickets(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _usuario: UsuarioResponse = Depends(get_current_user),
):
    return crud_ticket.obtener_todos(db, skip, limit)


@router.put("/{ticket_id}", response_model=TicketResponse)
def actualizar_ticket(
    ticket_id: int,
    ticket_update: TicketUpdate,
    db: Session = Depends(get_db),
    _usuario: UsuarioResponse = Depends(get_current_user),
):
    ticket = crud_ticket.actualizar(db, ticket_id, ticket_update)
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket no encontrado")
    return ticket


@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_ticket(
    ticket_id: int, db: Session = Depends(get_db), _usuario: UsuarioResponse = Depends(get_current_user)
):
    if not crud_ticket.eliminar(db, ticket_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket no encontrado")
