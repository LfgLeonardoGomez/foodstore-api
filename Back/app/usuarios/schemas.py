from sqlmodel import SQLModel, Field
from pydantic import EmailStr

class UsuarioBase(SQLModel):
    username: str
    full_name: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    password: str


class UsuarioUpdate(UsuarioBase):
    password: str | None = None

class UsuarioRead(UsuarioBase):
    id: int
    role: str
    disabled: bool
    
class UsuarioPublico(UsuarioBase):
    id: int
    role: str
    disabled: bool

class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int  