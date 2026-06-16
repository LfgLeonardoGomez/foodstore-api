from typing import Annotated, List

from fastapi import APIRouter, Depends, status

from app.core.deps import get_current_active_user, require_role
from app.modules.usuarios.model import Usuario
from app.modules.usuarios.schemas import UsuarioList, UsuarioPublico, UsuarioRead, UsuarioUpdate
from app.modules.usuarios.service import UsuarioService


router = APIRouter(prefix="/api/v1", tags=["usuarios"])

service = UsuarioService()





@router.get("/admin/usuarios", response_model = UsuarioList)
def listar_usuarios(admin: Annotated[Usuario, Depends(require_role(["ADMIN"]))]):
    usuarios = service.traertodos()
    return usuarios

    #Actualiza perfil propio#

@router.put("/usuarios/me", response_model= UsuarioPublico)
def update_usuario(
    usuario_update: UsuarioUpdate,
    current_user: Annotated[Usuario, Depends(get_current_active_user)]
):
    service.es_admin_o_me(current_user, current_user.id)
    return service.actualizar_usuario(current_user.id, usuario_update)

    #Activa o desactva un usuario usuario (solo admin)#

@router.post("/usuarios/{usuario_id}/desactivar", response_model= UsuarioPublico)
def disable_usuario(
    usuario_id: int,
    es_admin: Annotated[Usuario, Depends(require_role(["ADMIN"]))]):
    return service.set_disabled(usuario_id, True)

@router.post("/usuarios/{usuario_id}/reactivar", response_model= UsuarioPublico)
def enable_usuario(
    usuario_id: int,
    es_admin: Annotated[Usuario, Depends(require_role(["ADMIN"]))]):
    return service.set_disabled(usuario_id, False)

    # Admin modifica roles de usuario (solo admin) #

@router.put("/admin/usuarios/{usuario_id}/roles", response_model= UsuarioRead, status_code=status.HTTP_200_OK)
def modificar_roles(
    usuario_id: int,
    roles: list[str],
    es_admin: Annotated[Usuario, Depends(require_role(["ADMIN"]))]):
    return service.modificar_roles(usuario_id, roles)

    # Admin puede ver detalle de un usuario #

@router.get("/admin/usuarios/{usuario_id}", response_model= UsuarioPublico)
def get_usuario(
    usuario_id: int,
    es_admin: Annotated[Usuario, Depends(require_role(["ADMIN"]))]):
    return service.traer_por_id(usuario_id)


