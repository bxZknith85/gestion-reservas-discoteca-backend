"""Endpoints para gestión de usuarios"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from app.crud.usuario import CRUDUsuario

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """Crear un nuevo usuario"""
    usuario_existente = CRUDUsuario.obtener_por_email(db, usuario.email)
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email ya registrado"
        )
    
    return CRUDUsuario.crear(db, usuario)


@router.get("/{user_id}", response_model=UsuarioResponse)
def obtener_usuario(user_id: int, db: Session = Depends(get_db)):
    """Obtener un usuario por ID"""
    usuario = CRUDUsuario.obtener_por_id(db, user_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return usuario


@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar todos los usuarios"""
    return CRUDUsuario.obtener_todos(db, skip, limit)


@router.put("/{user_id}", response_model=UsuarioResponse)
def actualizar_usuario(user_id: int, usuario_update: UsuarioUpdate, db: Session = Depends(get_db)):
    """Actualizar un usuario"""
    usuario = CRUDUsuario.actualizar(db, user_id, usuario_update)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return usuario


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(user_id: int, db: Session = Depends(get_db)):
    """Eliminar un usuario"""
    if not CRUDUsuario.eliminar(db, user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
