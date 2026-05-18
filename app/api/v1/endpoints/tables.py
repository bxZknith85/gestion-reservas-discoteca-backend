"""Endpoints para gestión de mesas"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.endpoints.auth import get_current_user
from app.crud import table as crud_table
from app.db.database import get_db
from app.schemas.table import DicoTableCreate, DicoTableResponse, DicoTableUpdate
from app.schemas.usuario import UsuarioResponse

router = APIRouter(prefix="/tables", tags=["tables"])


@router.post("/", response_model=DicoTableResponse, status_code=status.HTTP_201_CREATED)
def crear_mesa(
    mesa: DicoTableCreate, db: Session = Depends(get_db), _usuario: UsuarioResponse = Depends(get_current_user)
):
    """Crear una nueva mesa"""
    if crud_table.obtener_por_numero(db, mesa.number):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"Ya existe una mesa con el número {mesa.number}"
        )
    return crud_table.crear(db, mesa)


@router.get("/{table_id}", response_model=DicoTableResponse)
def obtener_mesa(table_id: int, db: Session = Depends(get_db), _usuario: UsuarioResponse = Depends(get_current_user)):
    """Obtener una mesa por ID"""
    mesa = crud_table.obtener_por_id(db, table_id)
    if not mesa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mesa no encontrada")
    return mesa


@router.get("/", response_model=list[DicoTableResponse])
def listar_mesas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _usuario: UsuarioResponse = Depends(get_current_user),
):
    """Listar todas las mesas"""
    return crud_table.obtener_todas(db, skip, limit)


@router.put("/{table_id}", response_model=DicoTableResponse)
def actualizar_mesa(
    table_id: int,
    mesa_update: DicoTableUpdate,
    db: Session = Depends(get_db),
    _usuario: UsuarioResponse = Depends(get_current_user),
):
    """Actualizar una mesa"""
    mesa = crud_table.actualizar(db, table_id, mesa_update)
    if not mesa:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mesa no encontrada")
    return mesa


@router.delete("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_mesa(table_id: int, db: Session = Depends(get_db), _usuario: UsuarioResponse = Depends(get_current_user)):
    """Eliminar una mesa"""
    if not crud_table.eliminar(db, table_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mesa no encontrada")
