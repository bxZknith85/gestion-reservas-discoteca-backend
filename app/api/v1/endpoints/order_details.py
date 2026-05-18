from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import order_detail as crud_order_detail
from app.db.database import get_db
from app.schemas.order_detail import (
    OrderDetailCreate,
    OrderDetailResponse,
    OrderDetailUpdate,
)

router = APIRouter(prefix="/order-details", tags=["order-details"])


@router.post("/", response_model=OrderDetailResponse, status_code=status.HTTP_201_CREATED)
def crear(obj: OrderDetailCreate, db: Session = Depends(get_db)):
    return crud_order_detail.crear(db, obj)


@router.get("/{id}", response_model=OrderDetailResponse)
def obtener(id: int, db: Session = Depends(get_db)):
    obj = crud_order_detail.obtener_por_id(db, id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Detalle de orden no encontrado")
    return obj


@router.get("/order/{order_id}", response_model=list[OrderDetailResponse])
def listar_por_orden(order_id: int, db: Session = Depends(get_db)):
    return crud_order_detail.obtener_por_orden(db, order_id)


@router.get("/", response_model=list[OrderDetailResponse])
def listar(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_order_detail.obtener_todos(db, skip, limit)


@router.put("/{id}", response_model=OrderDetailResponse)
def actualizar(id: int, obj_update: OrderDetailUpdate, db: Session = Depends(get_db)):
    obj = crud_order_detail.actualizar(db, id, obj_update)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Detalle de orden no encontrado")
    return obj


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(id: int, db: Session = Depends(get_db)):
    if not crud_order_detail.eliminar(db, id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Detalle de orden no encontrado")
