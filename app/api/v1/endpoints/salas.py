from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.sala import SalaCreate, SalaResponse, SalaUpdate
from app.crud.sala import CRUDSala

router = APIRouter(prefix="/salas", tags=["salas"])


@router.post("/", response_model=SalaResponse)
def crear_sala(sala: SalaCreate, db: Session = Depends(get_db)):
    """Crear una nueva sala"""
    return CRUDSala.crear(db, sala)


@router.get("/{sala_id}", response_model=SalaResponse)
def obtener_sala(sala_id: int, db: Session = Depends(get_db)):
    """Obtener una sala por ID"""
    sala = CRUDSala.obtener_por_id(db, sala_id)
    if not sala:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    return sala


@router.get("/", response_model=list[SalaResponse])
def listar_salas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar todas las salas"""
    return CRUDSala.obtener_todas(db, skip, limit)


@router.put("/{sala_id}", response_model=SalaResponse)
def actualizar_sala(sala_id: int, sala_update: SalaUpdate, db: Session = Depends(get_db)):
    """Actualizar una sala"""
    sala = CRUDSala.actualizar(db, sala_id, sala_update)
    if not sala:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    return sala


@router.delete("/{sala_id}")
def eliminar_sala(sala_id: int, db: Session = Depends(get_db)):
    """Eliminar una sala"""
    if not CRUDSala.eliminar(db, sala_id):
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    return {"message": "Sala eliminada exitosamente"}
