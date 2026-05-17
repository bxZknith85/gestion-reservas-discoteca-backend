from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.table_price import TablePriceCreate, TablePriceResponse, TablePriceUpdate
from app.crud import table_price as crud_table_price

router = APIRouter(prefix="/table-prices", tags=["table-prices"])


@router.post("/", response_model=TablePriceResponse, status_code=status.HTTP_201_CREATED)
def crear(obj: TablePriceCreate, db: Session = Depends(get_db)):
    return crud_table_price.crear(db, obj)


@router.get("/{id}", response_model=TablePriceResponse)
def obtener(id: int, db: Session = Depends(get_db)):
    obj = crud_table_price.obtener_por_id(db, id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Precio de mesa no encontrado")
    return obj


@router.get("/event/{event_id}", response_model=list[TablePriceResponse])
def listar_por_evento(event_id: int, db: Session = Depends(get_db)):
    return crud_table_price.obtener_por_evento(db, event_id)


@router.get("/table/{table_id}", response_model=list[TablePriceResponse])
def listar_por_mesa(table_id: int, db: Session = Depends(get_db)):
    return crud_table_price.obtener_por_mesa(db, table_id)


@router.get("/", response_model=list[TablePriceResponse])
def listar(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_table_price.obtener_todos(db, skip, limit)


@router.put("/{id}", response_model=TablePriceResponse)
def actualizar(id: int, obj_update: TablePriceUpdate, db: Session = Depends(get_db)):
    obj = crud_table_price.actualizar(db, id, obj_update)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Precio de mesa no encontrado")
    return obj


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(id: int, db: Session = Depends(get_db)):
    if not crud_table_price.eliminar(db, id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Precio de mesa no encontrado")
