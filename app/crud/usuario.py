from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.core.security import get_password_hash, verify_password


class CRUDUsuario:
    @staticmethod
    def crear(db: Session, usuario: UsuarioCreate) -> Usuario:
        db_usuario = Usuario(
            email=usuario.email,
            username=usuario.username,
            nombre_completo=usuario.nombre_completo,
            numero_telefono=usuario.numero_telefono,
            hashed_password=get_password_hash(usuario.password),
        )
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    
    @staticmethod
    def obtener_por_id(db: Session, usuario_id: int) -> Usuario:
        return db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    @staticmethod
    def obtener_por_email(db: Session, email: str) -> Usuario:
        return db.query(Usuario).filter(Usuario.email == email).first()
    
    @staticmethod
    def obtener_por_username(db: Session, username: str) -> Usuario:
        return db.query(Usuario).filter(Usuario.username == username).first()
    
    @staticmethod
    def obtener_todos(db: Session, skip: int = 0, limit: int = 100) -> list[Usuario]:
        return db.query(Usuario).offset(skip).limit(limit).all()
    
    @staticmethod
    def actualizar(db: Session, usuario_id: int, usuario_update: UsuarioUpdate) -> Usuario:
        db_usuario = CRUDUsuario.obtener_por_id(db, usuario_id)
        if db_usuario:
            update_data = usuario_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_usuario, key, value)
            db.add(db_usuario)
            db.commit()
            db.refresh(db_usuario)
        return db_usuario
    
    @staticmethod
    def eliminar(db: Session, usuario_id: int) -> bool:
        db_usuario = CRUDUsuario.obtener_por_id(db, usuario_id)
        if db_usuario:
            db.delete(db_usuario)
            db.commit()
            return True
        return False
    
    @staticmethod
    def autenticar(db: Session, email: str, password: str) -> Usuario:
        usuario = CRUDUsuario.obtener_por_email(db, email)
        if not usuario:
            return None
        if not verify_password(password, usuario.hashed_password):
            return None
        return usuario
