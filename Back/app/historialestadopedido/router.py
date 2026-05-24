from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.core.deps import get_current_active_user, require_role,get_current_user
from app.historialestadopedido.schema import (
    HistorialPedidoEstadoCreate,
    HistorialPedidoEstadoRead,
)
from app.historialestadopedido.service import HistorialEstadoPedidoService



router = APIRouter(prefix="/historialpedidos", tags=["Historial Estado Pedido"])
service = HistorialEstadoPedidoService()

@router.post(
    "/{pedido_id}/historial",
    response_model=HistorialPedidoEstadoRead,
    status_code=status.HTTP_201_CREATED,
)
def registrar_transicion(
    pedido_id: int,
    payload: HistorialPedidoEstadoCreate,
    current_user=Depends(get_current_active_user)
):
    return service.registrar_transicion(
        pedido_id=pedido_id,
        estado_hacia=payload.estado_hacia,
        usuario_id=current_user.id,
        roles=[r.codigo for r in current_user.roles],
        motivo=payload.motivo,
    )


@router.get(
    "/{pedido_id}/historial",
    response_model=list[HistorialPedidoEstadoRead],
    status_code=status.HTTP_200_OK,
)
def get_historial_by_pedido(
    pedido_id: int,
    current_user=Depends(get_current_user)
):
    return service.get_historial_by_pedido(pedido_id)


@router.get(
    "/historial/{historial_id}",
    response_model=HistorialPedidoEstadoRead,
    status_code=status.HTTP_200_OK,
)
def get_by_id(
    historial_id: int,
    current_user=Depends(get_current_user)
):
    return service.get_by_id(historial_id)