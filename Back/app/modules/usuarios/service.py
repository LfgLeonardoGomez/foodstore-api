
from typing import Optional, List
from fastapi import HTTPException, status
from app.core.security import hash_password
from app.core.uow import UnitOfWork
from app.modules.usuarios.model import Usuario
from app.modules.usuarios.schemas import UsuarioList, UsuarioPublico, UsuarioRead, UsuarioUpdate


class UsuarioService:
    def __init__(self):
        self.uow = UnitOfWork()

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

            updated = uow.usuarios.update(usuario_db)
            return UsuarioPublico.model_validate({
                "id": updated.id,
                "nombre": updated.nombre,
                "apellido": updated.apellido,
                "email": updated.email,
                "celular": updated.celular,
                "disabled": updated.disabled,
                "roles": [rol.codigo for rol in updated.roles]
            })

    def traertodos(self) -> UsuarioList:
            with UnitOfWork() as uow:
                data = uow.usuarios.get_all(0,20)
                return UsuarioList(
                    data=[UsuarioPublico.model_validate({
                        "id": u.id,
                        "nombre": u.nombre,
                        "apellido": u.apellido,
                        "email": u.email,
                        "celular": u.celular,
                        "disabled": u.disabled,
                        "roles": [rol.codigo for rol in u.roles]
                    }) for u in data],
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
                return UsuarioPublico.model_validate({
                    "id": usuario.id,
                    "nombre": usuario.nombre,
                    "apellido": usuario.apellido,
                    "email": usuario.email,
                    "celular": usuario.celular,
                    "disabled": usuario.disabled,
                    "roles": [rol.codigo for rol in usuario.roles]
                })
            
    def traer_por_email(self, email: str) -> Optional[Usuario]:
            with UnitOfWork() as uow:
                usuario = uow.usuarios.get_by_email(email)
                if not usuario:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Usuario no encontrado"
                    )
                return UsuarioPublico.model_validate({
                    "id": usuario.id,
                    "nombre": usuario.nombre,
                    "apellido": usuario.apellido,
                    "email": usuario.email,
                    "celular": usuario.celular,
                    "disabled": usuario.disabled,
                    "roles": [rol.codigo for rol in usuario.roles]
                })
            
    def set_disabled(self, usuario_id: int, disabled: bool) -> UsuarioPublico:
            with UnitOfWork() as uow:
                usuario = uow.usuarios.get_by_id_including_disabled(usuario_id)
                if not usuario:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Usuario no encontrado"
                    )
                usuario.disabled = disabled
                uow.usuarios.update(usuario)
                return UsuarioPublico.model_validate({
                    "id": usuario.id,
                    "nombre": usuario.nombre,
                    "apellido": usuario.apellido,
                    "email": usuario.email,
                    "celular": usuario.celular,
                    "disabled": usuario.disabled,
                    "roles": [rol.codigo for rol in usuario.roles]
                })   

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