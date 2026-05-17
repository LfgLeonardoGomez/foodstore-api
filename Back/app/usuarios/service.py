
import email
from typing import Optional, List
from fastapi import HTTPException, status
from app.core.config import Settings
from app.core.security import create_access_token, hash_password
from app.core.uow import UnitOfWork
from app.usuarios.model import Usuario
from app.usuarios.schemas import Token, UsuarioCreate, UsuarioPublico, UsuarioRead


class ProductoService:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def crear_usuario(self, usuario: UsuarioCreate):
        with UnitOfWork() as uow:
            if uow.usuarios.get_by_username(usuario.username):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username ya existe"
                )
            
            if uow.usuarios.get_by_email(usuario.email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email ya existe"
                )
            
            usuario_db = Usuario(
                username = usuario.username,
                full_name = usuario.full_name,
                email = usuario.email,
                password = hash_password(usuario.password),
                rol = "user"
            )
            rta = UsuarioPublico.model_validate(self.uow.usuarios.add(usuario_db))
            return rta


    def actualizar_usuario(self, usuario_id: int, usuario: UsuarioCreate):
        with UnitOfWork() as uow:
            usuario_db = uow.usuarios.get_by_id(usuario_id)
            if not usuario_db:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado",
                    )
            
            if usuario_db.username != usuario.username and uow.usuarios.get_by_username(usuario.username):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username ya existe"
                )
            if usuario_db.email != usuario.email and uow.usuarios.get_by_email(usuario.email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email ya existe"
                )
            
            usuario_db.username = usuario.username
            usuario_db.full_name = usuario.full_name
            usuario_db.email = usuario.email
            if usuario.password:
                usuario_db.password = hash_password(usuario.password)
            rta = UsuarioPublico.model_validate(self.uow.usuarios.update(usuario_db))
            return rta
        
    
    def autenticar_usuario(self, username: str, password: str) -> Token:
        with UnitOfWork() as uow:
            usuario = self.uow.usuarios.get_by_username(username)
            if not usuario or not usuario.verify_password(password):
                raise HTTPException (
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciales inválidas",
                    headers={"WWW-Authenticate": "Bearer"}
                )
            if usuario.disabled:
                raise HTTPException (
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Usuario deshabilitado"
                )
            
            acces_token = create_access_token(data={"sub": usuario.username, "rol": usuario.rol})

            return Token(access_token = acces_token, token_type="bearer", expires_in = Settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
        

        def traertodos(self) -> list[Usuario]:
            with UnitOfWork() as uow:
                return uow.usuarios.get_all(0,20)
            
        
        def traer_por_username(self, username: str) -> Optional[Usuario]:
            with UnitOfWork() as uow:
                return uow.usuarios.get_by_username(username)
            
        def traer_por_email(self, email: str) -> Optional[Usuario]:
            with UnitOfWork() as uow:
                return uow.usuarios.get_by_email(email)
            
        def set_disabled(self, usuario_id: int, disabled: bool) -> Usuario:
            with UnitOfWork() as uow:
                usuario = uow.usuarios.get_by_id(usuario_id)
                if not usuario:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Usuario no encontrado"
                    )
                usuario.disabled = disabled
                return uow.usuarios.update(usuario)
            
        