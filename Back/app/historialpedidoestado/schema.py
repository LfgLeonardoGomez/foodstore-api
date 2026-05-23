


from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class HistorialPedidoEstadoBase(BaseModel):
    estado_desde: Optional[str] = None
    estado_hacia: str
    usuario_id: int
    pedido_id: int
    motivo: Optional[str] = None


class HistorialPedidoEstadoCreate(HistorialPedidoEstadoBase):
    pass

class HistorialPedidoEstadoRead(HistorialPedidoEstadoBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

