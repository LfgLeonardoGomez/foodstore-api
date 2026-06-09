from fastapi import HTTPException, status

from app.core.uow import UnitOfWork
from app.historialestadopedido.model import HistorialEstadoPedido


class HistorialEstadoPedidoService:

    def registrar_transicion(
        self,
        pedido_id: int,
        estado_hacia: str,
        usuario_id: int,
        roles: list[str],
        motivo: str | None = None,
    ) -> dict:
        with UnitOfWork() as uow:
            pedido = uow.pedidos.get_by_id(pedido_id)

            if not pedido:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Pedido no encontrado.",
                )

            estado_desde = pedido.cambiar_estado(
                estado_hacia=estado_hacia,
                roles=roles,
                motivo=motivo,
            )

            nuevo_registro = uow.historialestadopedido.create(
                HistorialEstadoPedido(
                    pedido_id=pedido.id,
                    estado_desde=estado_desde,
                    estado_hacia=pedido.estado_codigo,
                    usuario_id=usuario_id,
                    motivo=motivo,
                )
            )

            return {
                "id": nuevo_registro.id,
                "pedido_id": nuevo_registro.pedido_id,
                "estado_desde": nuevo_registro.estado_desde,
                "estado_hacia": nuevo_registro.estado_hacia,
                "usuario_id": nuevo_registro.usuario_id,
                "motivo": nuevo_registro.motivo,
                "created_at": nuevo_registro.created_at,
            }

    def get_historial_by_pedido(self, pedido_id: int) -> list:
        with UnitOfWork() as uow:
            historial = uow.historialestadopedido.get_by_pedido_id(pedido_id)

            return [{
                "id": h.id,
                "pedido_id": h.pedido_id,
                "estado_desde": h.estado_desde,
                "estado_hacia": h.estado_hacia,
                "usuario_id": h.usuario_id,
                "motivo": h.motivo,
                "created_at": h.created_at,
            } for h in historial]

    def get_by_id(self, historial_id: int) -> HistorialEstadoPedido:
        with UnitOfWork() as uow:
            registro = uow.historialestadopedido.get_by_id(historial_id)

            if not registro:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Registro de historial {historial_id} no encontrado.",
                )

            return registro


historialestadopedidoservice = HistorialEstadoPedidoService()