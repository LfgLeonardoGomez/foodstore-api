from decimal import Decimal

from sqlmodel import Field, Relationship, SQLModel

from app.detallepedido.model import DetallePedido
from app.direccioentrega.model import DireccionEntrega
from app.historialestadopedido.model import HistorialEstadoPedido
from app.usuarios.model import Usuario


class Pedido(SQLModel, table=True):
    __tablename__ = "pedidos"

    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuarios.id", nullable=False)
    direccion_id: int = Field(foreign_key="direcciones.id", nullable=False)
    estado_codigo: str = Field(foreign_key="estado_pedido.codigo", nullable=False)
    forma_pago_codigo: str = Field(foreign_key="forma_de_pago.codigo", nullable=False)
    
    #---------------------------------------#
    #     snpshot      #
    #---------------------------------------#
    subtotal: Decimal = Field(nullable=False)
    descuento: Decimal = Field(nullable=False, default=Decimal("0.00"))
    costo_envio: Decimal = Field(nullable=False, default=Decimal("50.00"))
    total: Decimal = Field(nullable=False, ge = 0)

    notas: str | None = Field(default=None)

    detalles: list["DetallePedido"] = Relationship(back_populates="pedido")
    usuario: "Usuario" = Relationship(back_populates="pedidos")
    direccion: "DireccionEntrega" = Relationship(back_populates="pedidos")
    historial_estado: list["HistorialEstadoPedido"] = Relationship(back_populates="pedido")