from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.usuario import CRUDUsuario
from app.db.database import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.post("/", response_model=UsuarioResponse)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """Crear un nuevo usuario"""
    usuario_existente = CRUDUsuario.obtener_por_email(db, usuario.email)
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    usuario_existente = CRUDUsuario.obtener_por_username(db, usuario.username)
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Username ya existe")

    return CRUDUsuario.crear(db, usuario)


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Obtener un usuario por ID"""
    usuario = CRUDUsuario.obtener_por_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar todos los usuarios"""
    return CRUDUsuario.obtener_todos(db, skip, limit)


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(usuario_id: int, usuario_update: UsuarioUpdate, db: Session = Depends(get_db)):
    """Actualizar un usuario"""
    usuario = CRUDUsuario.actualizar(db, usuario_id, usuario_update)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Eliminar un usuario"""
    if not CRUDUsuario.eliminar(db, usuario_id):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado exitosamente"}
