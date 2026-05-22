
import email
from typing import Optional, List
from fastapi import HTTPException, status
from app.core.config import settings
from app.core.security import create_access_token, hash_password, verify_password
from app.core.uow import UnitOfWork
from app.usuarios.model import Usuario
from app.usuarios.schemas import Token, UsuarioCreate, UsuarioList, UsuarioPublico, UsuarioRead, UsuarioUpdate


class UsuarioService:
    def __init__(self):
        self.uow = UnitOfWork()

# ● Registro de usuarios con asignación automática del rol CLIENT
# ● Login con email/password → genera cookie “access token” (JWT, 30 min)
# ● Endpoint GET /me para obtener datos del usuario autenticado 



    def crear_usuario(self, usuario: UsuarioCreate):
        with UnitOfWork() as uow:
        
            if uow.usuarios.get_by_email(usuario.email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email ya existe"
                )
            rol_client = uow.roles.get_by_codigo("CLIENT")

            usuario_db = Usuario(
                nombre= usuario.nombre,
                apellido = usuario.apellido,
                email = usuario.email,
                celular = usuario.celular,
                password_hashed= hash_password(usuario.password),
                disabled=False,
                roles = [rol_client]

            )
            rta = uow.usuarios.create(usuario_db)
            return UsuarioPublico.model_validate(rta)



    def actualizar_usuario(self, usuario_id: int, usuario: UsuarioUpdate):
        
        with UnitOfWork() as uow:

            usuario_db = uow.usuarios.get_by_id(usuario_id)
            if not usuario_db:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado",
                    )
        
            if usuario_db.email != usuario.email and uow.usuarios.get_by_email(usuario.email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email ya existe"
                )
            
            update_data = usuario.model_dump(exclude_unset=True)
            password = update_data.pop("password", None)

            if password:
                usuario_db.password_hashed = hash_password(password)

            for key, value in update_data.items():
                setattr(usuario_db, key, value)

            return UsuarioPublico.model_validate(uow.usuarios.update(usuario_db))
        
    
    def autenticar_usuario(self, email: str, password: str) -> Token:
        with UnitOfWork() as uow:

            usuario = uow.usuarios.get_by_email(email)

            if not usuario or not verify_password(password, usuario.password_hashed):
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
            
            acces_token = create_access_token(
                data={"sub": usuario.email, "roles": [rol.codigo for rol in usuario.roles]})

            return Token(access_token = acces_token,
                        token_type="bearer",
                         expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
        

    def traertodos(self) -> UsuarioList:
            with UnitOfWork() as uow:
                data = uow.usuarios.get_all(0,20)
                return UsuarioList(
                    data=[UsuarioPublico.model_validate(u) for u in data],
                    count=len(data)
                )
    def traer_por_id(self, usuario_id: int) -> UsuarioPublico:
            with UnitOfWork() as uow:
                usuario = uow.usuarios.get_by_id(usuario_id)
                if not usuario:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Usuario no encontrado"
                    )
                return UsuarioPublico.model_validate(usuario)
            
    def traer_por_email(self, email: str) -> Optional[Usuario]:
            with UnitOfWork() as uow:
                usuario = uow.usuarios.get_by_email(email)
                if not usuario:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Usuario no encontrado"
                    )
                return UsuarioPublico.model_validate(usuario)
            
    def set_disabled(self, usuario_id: int, disabled: bool) -> UsuarioPublico:
            with UnitOfWork() as uow:
                usuario = uow.usuarios.get_by_id_including_disabled(usuario_id)
                if not usuario:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Usuario no encontrado"
                    )
                usuario.disabled = disabled
                return UsuarioPublico.model_validate(uow.usuarios.update(usuario))   

    def modificar_roles(self, usuario_id: int, roles: List[str]) :
        with UnitOfWork() as uow:
            usuario = uow.usuarios.get_by_id(usuario_id)
            if not usuario:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado"
                )
            if not roles:
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El usuario debe tener al menos un rol"
                    )
            nuevos_roles = []
            for codigo in roles:
                rol = uow.roles.get_by_codigo(codigo.upper())
                if not rol:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Rol '{codigo}' no existe"
                    )
                nuevos_roles.append(rol)
            usuario.roles = nuevos_roles
            usuario_db = uow.usuarios.update(usuario)
            return self._to_usuario_read(usuario_db)

    def es_admin_o_me(self, current_user: Usuario, usuario_id: int) -> bool:
        es_admin = any(rol.codigo == "ADMIN" for rol in current_user.roles)
        es_me = current_user.id == usuario_id
        if not (es_admin or es_me):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para realizar esta acción"
            )
        return True
        
    def _to_usuario_read(self, usuario: Usuario) -> UsuarioRead:
        return UsuarioRead(
            id=usuario.id,
            nombre=usuario.nombre,
            apellido=usuario.apellido,
            email=usuario.email,
            celular=usuario.celular,
            disabled=usuario.disabled,
            roles=[rol.codigo for rol in usuario.roles],
    )
    
usuario_service = UsuarioService()