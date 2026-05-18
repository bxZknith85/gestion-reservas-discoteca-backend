from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import order as crud_order
from app.crud import payment as crud_payment
from app.db.database import get_db
from app.schemas.order import OrderCreate, OrderResponse, OrderUpdate
from app.schemas.payment import PaymentCreate, PaymentResponse, PaymentUpdate

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def crear(obj: OrderCreate, db: Session = Depends(get_db)):
    return crud_order.crear(db, obj)


@router.get("/{id}", response_model=OrderResponse)
def obtener(id: int, db: Session = Depends(get_db)):
    obj = crud_order.obtener_por_id(db, id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")
    return obj


@router.get("/user/{user_id}", response_model=list[OrderResponse])
def listar_por_usuario(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_order.obtener_por_usuario(db, user_id, skip, limit)


@router.get("/", response_model=list[OrderResponse])
def listar(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_order.obtener_todos(db, skip, limit)


@router.put("/{id}", response_model=OrderResponse)
def actualizar(id: int, obj_update: OrderUpdate, db: Session = Depends(get_db)):
    obj = crud_order.actualizar(db, id, obj_update)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")
    return obj


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(id: int, db: Session = Depends(get_db)):
    if not crud_order.eliminar(db, id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")


@router.post("/{order_id}/payments/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def crear_pago(_order_id: int, obj: PaymentCreate, db: Session = Depends(get_db)):
    return crud_payment.crear(db, obj)


@router.get("/{order_id}/payments/", response_model=list[PaymentResponse])
def listar_pagos(order_id: int, db: Session = Depends(get_db)):
    return crud_payment.obtener_por_orden(db, order_id)


@router.put("/payments/{payment_id}", response_model=PaymentResponse)
def actualizar_pago(payment_id: int, obj_update: PaymentUpdate, db: Session = Depends(get_db)):
    obj = crud_payment.actualizar(db, payment_id, obj_update)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pago no encontrado")
    return obj
