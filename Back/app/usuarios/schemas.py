from sqlmodel import SQLModel, Field


class UsuarioBase(SQLModel):

    nombre : str = Field(nullable=False)
    apellido : str = Field(nullable=False)
    email: str
    celular : str = Field(max_length=20)


class UsuarioCreate(UsuarioBase):
    password_hashed: str


class UsuarioUpdate(UsuarioBase):
    password_hashed: str | None = None

class UsuarioRead(UsuarioBase):
    id: int
    roles: list[str] = Field(default_factory=list)
    disabled: bool
    
class UsuarioPublico(UsuarioBase):
    id: int

    roles: list[str] = Field(default_factory=list)
    disabled: bool

class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int  