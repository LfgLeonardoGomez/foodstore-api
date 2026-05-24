
from typing import Optional

from sqlmodel import SQLModel, Field


class EstadoPedido (SQLModel, table = True):
    __tablename__ = "estado_pedido"
    codigo : str = Field(primary_key=True)
    descripcion : str = Field(min_length= 3, max_length= 100, nullable=False)
    orden : int = Field(nullable=False, unique=True)
    es_terminal: bool = Field (default=False, nullable=False)
    

