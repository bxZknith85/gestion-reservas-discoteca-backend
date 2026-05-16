"""Endpoints para gestión de mesas"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.table import DicoTableCreate, DicoTableResponse, DicoTableUpdate
from app.crud.sala import CRUDSala

router = APIRouter(prefix="/tables", tags=["tables"])


@router.post("/", response_model=DicoTableResponse, status_code=status.HTTP_201_CREATED)
def crear_mesa(mesa: DicoTableCreate, db: Session = Depends(get_db)):
    """Crear una nueva mesa"""
    return CRUDSala.crear(db, mesa)


@router.get("/{table_id}", response_model=DicoTableResponse)
def obtener_mesa(table_id: int, db: Session = Depends(get_db)):
    """Obtener una mesa por ID"""
    mesa = CRUDSala.obtener_por_id(db, table_id)
    if not mesa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mesa no encontrada"
        )
    return mesa


@router.get("/", response_model=list[DicoTableResponse])
def listar_mesas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar todas las mesas"""
    return CRUDSala.obtener_todas(db, skip, limit)


@router.put("/{table_id}", response_model=DicoTableResponse)
def actualizar_mesa(table_id: int, mesa_update: DicoTableUpdate, db: Session = Depends(get_db)):
    """Actualizar una mesa"""
    mesa = CRUDSala.actualizar(db, table_id, mesa_update)
    if not mesa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mesa no encontrada"
        )
    return mesa


@router.delete("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_mesa(table_id: int, db: Session = Depends(get_db)):
    """Eliminar una mesa"""
    if not CRUDSala.eliminar(db, table_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mesa no encontrada"
        )
