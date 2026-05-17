from sqlalchemy.orm import Session
from app.models.core import User
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.core.security import get_password_hash, verify_password


class CRUDUsuario:
    @staticmethod
    def crear(db: Session, usuario: UsuarioCreate) -> User:
        db_usuario = User(
            email=usuario.email,
            username=usuario.username,
            phone_number=usuario.phone_number,
            password_hash=get_password_hash(usuario.password),
            type_user_id=usuario.type_user_id,
            is_active=True
        )
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    
    @staticmethod
    def obtener_por_id(db: Session, usuario_id: int) -> User:
        return db.query(User).filter(User.id == usuario_id).first()
    
    @staticmethod
    def obtener_por_email(db: Session, email: str) -> User:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def obtener_por_telefono(db: Session, phone_number: str) -> User:
        return db.query(User).filter(User.phone_number == phone_number).first()
    
    @staticmethod
    def obtener_por_username(db: Session, username: str) -> User:
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def obtener_todos(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
        return db.query(User).offset(skip).limit(limit).all()
    
    @staticmethod
    def actualizar(db: Session, usuario_id: int, usuario_update: UsuarioUpdate) -> User:
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
    def autenticar(db: Session, email: str, password: str) -> User:
        usuario = CRUDUsuario.obtener_por_email(db, email)
        if not usuario:
            return None
        if not verify_password(password, usuario.password_hash):
            return None
        return usuario
