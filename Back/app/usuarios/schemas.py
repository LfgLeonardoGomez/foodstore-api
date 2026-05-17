from sqlmodel import SQLModel, Field
from pydantic import EmailStr

class UsuarioBase(SQLModel):
    nombre: str
    apellido: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    password_hashed: str


class UsuarioUpdate(UsuarioBase):
    password_hashed: str | None = None

class UsuarioRead(UsuarioBase):
    id: int
    roles: str 
    disabled: bool
    
class UsuarioPublico(UsuarioBase):
    id: int
    roles: str
    disabled: bool

class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int  