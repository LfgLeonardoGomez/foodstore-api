from fastapi import HTTPException, status

from app.core.uow import UnitOfWork
from app.historialestadopedido.model import HistorialEstadoPedido


TRANSICIONES_VALIDAS: dict[str | None, list[str]] = {
    None:          ["PENDIENTE"],
    "PENDIENTE":   ["CONFIRMADO", "CANCELADO"],
    "CONFIRMADO":  ["EN_PREP", "CANCELADO"],
    "EN_PREP":     ["LISTO", "CANCELADO"],
    "LISTO":       ["ENTREGADO"],
    "ENTREGADO":   [],
    "CANCELADO":   [],
}

ESTADOS_TERMINALES = {"ENTREGADO", "CANCELADO"}
ROLES_CANCELACION_EN_PREP = {"ADMIN", "PEDIDOS"}


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
            estado_actual = self._get_estado_actual(pedido_id, uow)
            if estado_actual:
                estado_actual = estado_actual.upper()

            estado_hacia = estado_hacia.upper()

            self._validar_transicion(
                estado_desde=estado_actual,
                estado_hacia=estado_hacia,
                roles=roles,
            )

            if estado_hacia == "CANCELADO" and not motivo:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="El motivo es obligatorio para cancelar un pedido.",
                )

            nuevo_registro = uow.historialestadopedido.create(
                HistorialEstadoPedido(
                    pedido_id=pedido_id,
                    estado_desde=estado_actual,
                    estado_hacia=estado_hacia,
                    usuario_id=usuario_id,
                    motivo=motivo,
                )
            )

            pedido = uow.pedidos.get_by_id(pedido_id)
            pedido.estado_codigo = estado_hacia

            # Convertir a dict antes de que cierre la session
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
            # Convertir a dicts antes de que cierre la session
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

    def _get_estado_actual(self, pedido_id: int, uow: UnitOfWork) -> str | None:
        historial = uow.historialestadopedido.get_by_pedido_id(pedido_id)
        if not historial:
            return None
        return historial[-1].estado_hacia

    def _validar_transicion(
        self,
        estado_desde: str | None,
        estado_hacia: str,
        roles: list[str],
    ) -> None:
        if estado_desde in ESTADOS_TERMINALES:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"El pedido está en estado terminal '{estado_desde}' y no puede cambiar.",
            )

        transiciones = TRANSICIONES_VALIDAS.get(estado_desde, [])
        if estado_hacia not in transiciones:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"Transición inválida: '{estado_desde}' → '{estado_hacia}'. "
                    f"Transiciones permitidas: {transiciones}."
                ),
            )

        if estado_desde in {"EN_PREP"} and estado_hacia == "CANCELADO" and not any(r in ROLES_CANCELACION_EN_PREP for r in roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Solo un administrador puede cancelar un pedido en estado '{estado_desde}'.",
            )


historialestadopedidoservice = HistorialEstadoPedidoService()