

from datetime import datetime

from sqlmodel import Field, SQLModel
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column


class DetallePedidoBase(SQLModel):

    cantidad: int = Field(nullable=False, ge=1)
    nombre_snapshot: str = Field(nullable=False, max_length=200)
    precio_snapshot: float = Field(nullable=False, ge=0)
    subtotal_snapshot: float = Field(nullable=False, ge=0)
    personalizacion: list[list[int]] = Field(
        default_factory=list,
        sa_column=Column(JSONB, nullable=False),
    )

class DetallePedidoCreate(SQLModel):
    pedido_id: int
    producto_id: int
    cantidad: int = Field(ge=1)

    nombre_snapshot: str = Field(max_length=200)
    precio_snapshot: float = Field(ge=0)
    subtotal_snapshot: float = Field(ge=0)

    personalizacion: list[list[int]] = Field(default_factory=list)

class DetallePedidoRead(SQLModel):
    pedido_id: int
    producto_id: int

    cantidad: int

    nombre_snapshot: str
    precio_snapshot: float
    subtotal_snapshot: float

    personalizacion: list[list[int]]

    created_at: datetime

class DetallePedidoPublic(SQLModel):
    producto_id: int
    cantidad: int
    nombre_snapshot: str
    precio_snapshot: float
    subtotal_snapshot: float
    personalizacion: list[list[int]]

class DetallePedidoList(SQLModel):
    data: list[DetallePedidoPublic]
    count: int