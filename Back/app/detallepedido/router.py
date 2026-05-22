
from fastapi import APIRouter

from app.detallepedido.schema import DetallePedidoCreate, DetallePedidoList, DetallePedidoPublic
from app.detallepedido.service import DetallePedidoService


router = APIRouter(prefix="/api/v1/detallepedido", tags=["detallepedido"])

service = DetallePedidoService()

@router.post("/", response_model=DetallePedidoPublic)
def crear_detalle_pedido(detalle_pedido: DetallePedidoCreate):
    return service.crear_detalle_pedido(detalle_pedido)

@router.get("/pedido/{pedido_id}", response_model=DetallePedidoList)
def obtener_detalles_del_pedido(pedido_id: int, offset: int = 0, limit: int = 10):
    return service.obtener_detalles_del_pedido(pedido_id, offset=offset, limit=limit)

@router.get("/pedido/{pedido_id}/producto/{producto_id}", response_model=DetallePedidoPublic)
def obtener_detalle_por_id(pedido_id: int, producto_id: int):
    return service.obtener_detalle_por_id(pedido_id, producto_id)