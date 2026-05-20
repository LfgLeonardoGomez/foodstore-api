from sqlmodel import Relationship, SQLModel, Field
from typing import TYPE_CHECKING, List, Optional


from app.core.audit import AuditMixin
from app.core.models import UsuarioRol


if TYPE_CHECKING:
    from app.rol.model import Rol
if TYPE_CHECKING:
    from app.direccioentrega.model import DireccionEntrega

class Usuario (AuditMixin,SQLModel, table = True):
    __tablename__ = "usuarios"
    id:  int | None = Field(default=None, primary_key=True)
    nombre : str = Field(nullable=False)
    apellido : str = Field(nullable=False)
    email: str = Field(index=True, unique=True, nullable=False)
    celular : str = Field(max_length=20)
    password_hashed: str = Field(nullable=False)
    disabled: bool = Field(default=False)

    roles: List["Rol"] = Relationship(back_populates= "Usuarios",
                                    link_model=UsuarioRol)
    
    direcciones: List["DireccionEntrega"] = Relationship(
        back_populates="usuarios"
    )

