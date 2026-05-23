from fastapi import HTTPException, status

from app.historialpedidoestado.model import HistorialEstadoPedido
from app.historialpedidoestado.repository import HistorialPedidoEstadoRepository
from app.rol.model import Rol


# ---------------------------------------------------------------------------
# transiciones válidas por estado
# ---------------------------------------------------------------------------
TRANSICIONES_VALIDAS: dict[str | None, list[str]] = {
    None:          ["PENDIENTE"],       
    "PENDIENTE":   ["CONFIRMADO", "CANCELADO"],
    "CONFIRMADO":  ["EN_PREP", "CANCELADO"],
    "EN_PREP":     ["EN_CAMINO", "CANCELADO"],
    "EN_CAMINO":   ["ENTREGADO"],
    "ENTREGADO":   [],                   # terminal — RN-01
    "CANCELADO":   [],                   # terminal — RN-01
}

ESTADOS_TERMINALES = {"ENTREGADO", "CANCELADO"}

# Solo ADMIN puede cancelar desde EN_PREP (RN de la imagen)
ROLES_CANCELACION_EN_PREP  = {"ADMIN", "PEDIDOS"}


class HistorialEstadoPedidoService:

    def __init__(self, repository: HistorialPedidoEstadoRepository):
        self.repository = repository

    def registrar_transicion(
        self,
        pedido_id: int,
        estado_hacia: str,
        usuario_id: int,
        es_admin: bool = False,
        motivo: str | None = None,
        ) -> HistorialEstadoPedido:

        estado_actual = self._get_estado_actual(pedido_id)

        self._validar_transicion(
            estado_desde=estado_actual,
            estado_hacia=estado_hacia,
            es_admin=es_admin,
        )

        
        if estado_hacia == "CANCELADO" and not motivo:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="El motivo es obligatorio para cancelar un pedido.",
            )

        nuevo_registro = HistorialEstadoPedido(
            pedido_id=pedido_id,
            estado_desde=estado_actual,   # NULL si es la primera — RN-02
            estado_hacia=estado_hacia,
            usuario_id=usuario_id,
            motivo=motivo,
        )

        return self.repository.create(nuevo_registro)

    def get_historial_by_pedido(self, pedido_id: int) -> list[HistorialEstadoPedido]:
        return self.repository.get_by_pedido_id(pedido_id)

    def get_by_id(self, historial_id: int) -> HistorialEstadoPedido:
        registro = self.repository.get_by_id(historial_id)
        if not registro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Registro de historial {historial_id} no encontrado.",
            )
        return registro

#----------------------------------
#   metodos de ayuda             #
#----------------------------------
   
    def _get_estado_actual(self, pedido_id: int) -> str | None:
        
        historial = self.repository.get_by_pedido_id(pedido_id)
        if not historial:
            return None
        return historial[-1].estado_hacia

    def _validar_transicion(
        self,
        estado_desde: str | None,
        estado_hacia: str,
        es_admin: bool,
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

        
        if estado_desde in {"EN_PREP"} and estado_hacia == "CANCELADO" and Rol not in ROLES_CANCELACION_EN_PREP:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Solo un administrador puede cancelar un pedido en estado '{estado_desde}'.",
            )
        

historialestadopedidoservice = HistorialEstadoPedidoService()