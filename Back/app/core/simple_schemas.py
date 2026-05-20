from sqlmodel import SQLModel

class CategoriaSimple(SQLModel):
    id: int
    nombre: str

    model_config = {"from_attributes": True}


class ProductoSimple(SQLModel):
    id: int
    nombre: str

    model_config = {"from_attributes": True}

class IngredienteSimple(SQLModel):
    id: int
    nombre: str

    model_config = {"from_attributes": True}

class RolSimple(SQLModel):
    codigo: str
    model_config = {"from_attribute": True}

class UsuarioSimple(SQLModel):
    id: int
    nombre: str
    apellido: str
    email: str