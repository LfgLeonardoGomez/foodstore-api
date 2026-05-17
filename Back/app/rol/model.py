

from typing import List

from sqlmodel import Field, Relationship

from app.core.models import UsuarioRol
from app.usuarios.model import Usuario


class Rol: #No tiene que heredar SQLModel?
    __tablename__ = "roles"
    codigo : str = Field(max_length=20, nullable=False, primary_key=True)
    nombre : str = Field(unique=True, nullable=False, min_length=2, max_length=50)
    descripcion : str = Field(min_length= 3, max_length= 100, default=None)

    usuario_rol : List["Usuario"] = Relationship(back_populates="rol",
                                    link_model=UsuarioRol)