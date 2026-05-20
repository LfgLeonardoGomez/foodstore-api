

from sqlmodel import SQLModel


class DireccionEntregaBase(SQLModel):
    usuario_id: int
    alias: str
    linea_1: str
    linea_2: str
    ciudad: str
    provincia: str
    codigo_postal: str
    es_principal: bool

class DireccionEntregaCreate(DireccionEntregaBase):
    usuario_id: int
    pass

class DireccionEntregaUpdate(DireccionEntregaBase):
    pass

class DireccionEntregaRead(DireccionEntregaBase):
    id: int

class DireccionEntregaPublico(DireccionEntregaBase):
    id:int


