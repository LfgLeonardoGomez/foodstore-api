from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.limiter import limiter
from app.core.deps import get_current_active_user
from app.modules.usuarios.model import Usuario
from app.modules.usuarios.schemas import UsuarioCreate, UsuarioPublico
from app.modules.auth.schemas import Token
from app.modules.auth.service import AuthService

router = APIRouter(prefix="/api/v1", tags=["auth"])

service = AuthService()

#-------------------------------#
# Rutas de Autenticación
#-------------------------------#

@router.post("/register", response_model=UsuarioPublico, status_code=status.HTTP_201_CREATED)
@limiter.limit("100/15minute")
def register(usuario: UsuarioCreate, request: Request):
    return service.crear_usuario(usuario)


@router.post("/login", status_code=status.HTTP_200_OK)
@limiter.limit("100/15minute")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    request: Request,
    response: Response
):
    token = service.autenticar_usuario(form_data.username, form_data.password)
    response.set_cookie(key="access_token",
                        value=token.access_token,
                        httponly=True,
                        max_age=token.expires_in,
                        samesite="lax",
                        secure=False)
    return {"mensaje": "Inicio de sesión exitoso"}


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(response: Response):
    # Limpiar la cookie HttpOnly al cerrar sesión
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="lax",
        secure=False,
    )
    return {"mensaje": "Sesión cerrada exitosamente"}


@router.get("/me", response_model=UsuarioPublico)
def read_current_user(current_user: Annotated[Usuario,
                        Depends(get_current_active_user)]):
    return {
        "id": current_user.id,
        "nombre": current_user.nombre,
        "apellido": current_user.apellido,
        "email": current_user.email,
        "celular": current_user.celular,
        "disabled": current_user.disabled,
        "roles": [rol.codigo for rol in current_user.roles]
    }
