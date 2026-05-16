"""Endpoints para gestión de órdenes y pagos"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.order import OrderCreate, OrderResponse, OrderUpdate
from app.schemas.payment import PaymentCreate, PaymentResponse, PaymentUpdate

router = APIRouter(prefix="/orders", tags=["orders"])


# Endpoints de órdenes
@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def crear_orden(orden: OrderCreate, db: Session = Depends(get_db)):
    """Crear una nueva orden"""
    # TODO: Implementar CRUD de órdenes
    pass


@router.get("/{order_id}", response_model=OrderResponse)
def obtener_orden(order_id: int, db: Session = Depends(get_db)):
    """Obtener una orden por ID"""
    # TODO: Implementar CRUD de órdenes
    pass


@router.get("/", response_model=list[OrderResponse])
def listar_ordenes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar todas las órdenes"""
    # TODO: Implementar CRUD de órdenes
    pass


@router.put("/{order_id}", response_model=OrderResponse)
def actualizar_orden(order_id: int, orden_update: OrderUpdate, db: Session = Depends(get_db)):
    """Actualizar una orden"""
    # TODO: Implementar CRUD de órdenes
    pass


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_orden(order_id: int, db: Session = Depends(get_db)):
    """Eliminar una orden"""
    # TODO: Implementar CRUD de órdenes
    pass


# Endpoints de pagos
@router.post("/{order_id}/payments/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def crear_pago(order_id: int, pago: PaymentCreate, db: Session = Depends(get_db)):
    """Crear un nuevo pago para una orden"""
    # TODO: Implementar CRUD de pagos
    pass


@router.get("/{order_id}/payments/", response_model=list[PaymentResponse])
def listar_pagos_orden(order_id: int, db: Session = Depends(get_db)):
    """Listar todos los pagos de una orden"""
    # TODO: Implementar CRUD de pagos
    pass


@router.put("/payments/{payment_id}", response_model=PaymentResponse)
def actualizar_pago(payment_id: int, pago_update: PaymentUpdate, db: Session = Depends(get_db)):
    """Actualizar un pago (ej: confirmar pago)"""
    # TODO: Implementar CRUD de pagos
    pass
