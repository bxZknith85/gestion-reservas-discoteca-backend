from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.evento import EventoCreate, EventoResponse, EventoUpdate
from app.crud.evento import CRUDEvento

router = APIRouter(prefix="/eventos", tags=["eventos"])


@router.post("/", response_model=EventoResponse)
def crear_evento(evento: EventoCreate, db: Session = Depends(get_db)):
    """Crear un nuevo evento"""
    return CRUDEvento.crear(db, evento)


@router.get("/{evento_id}", response_model=EventoResponse)
def obtener_evento(evento_id: int, db: Session = Depends(get_db)):
    """Obtener un evento por ID"""
    evento = CRUDEvento.obtener_por_id(db, evento_id)
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return evento


@router.get("/", response_model=list[EventoResponse])
def listar_eventos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar todos los eventos"""
    return CRUDEvento.obtener_todos(db, skip, limit)


@router.put("/{evento_id}", response_model=EventoResponse)
def actualizar_evento(evento_id: int, evento_update: EventoUpdate, db: Session = Depends(get_db)):
    """Actualizar un evento"""
    evento = CRUDEvento.actualizar(db, evento_id, evento_update)
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return evento


@router.delete("/{evento_id}")
def eliminar_evento(evento_id: int, db: Session = Depends(get_db)):
    """Eliminar un evento"""
    if not CRUDEvento.eliminar(db, evento_id):
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return {"message": "Evento eliminado exitosamente"}
