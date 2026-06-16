from fastapi import HTTPException, status
from app.core.config import settings
from app.core.security import create_access_token, hash_password, verify_password
from app.core.uow import UnitOfWork
from app.modules.usuarios.model import Usuario
from app.modules.usuarios.schemas import UsuarioCreate, UsuarioPublico
from app.modules.auth.schemas import Token


class AuthService:
    def crear_usuario(self, usuario: UsuarioCreate):
        with UnitOfWork() as uow:

            if uow.usuarios.get_by_email(usuario.email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email ya existe"
                )
            rol_client = uow.roles.get_by_codigo("CLIENT")

            usuario_db = Usuario(
                nombre=usuario.nombre,
                apellido=usuario.apellido,
                email=usuario.email,
                celular=usuario.celular,
                password_hashed=hash_password(usuario.password),
                disabled=False,
                roles=[rol_client]
            )
            rta = uow.usuarios.create(usuario_db)
            return UsuarioPublico.model_validate({
                "id": rta.id,
                "nombre": rta.nombre,
                "apellido": rta.apellido,
                "email": rta.email,
                "celular": rta.celular,
                "disabled": rta.disabled,
                "roles": [rol.codigo for rol in rta.roles]
            })

    def autenticar_usuario(self, email: str, password: str) -> Token:
        with UnitOfWork() as uow:

            usuario = uow.usuarios.get_by_email(email)

            if not usuario or not verify_password(password, usuario.password_hashed):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciales inválidas",
                    headers={"WWW-Authenticate": "Bearer"}
                )
            if usuario.disabled:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Usuario deshabilitado"
                )

            acces_token = create_access_token(
                data={"sub": usuario.email, "roles": [rol.codigo for rol in usuario.roles]})

            return Token(access_token=acces_token,
                         token_type="bearer",
                         expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)


auth_service = AuthService()
