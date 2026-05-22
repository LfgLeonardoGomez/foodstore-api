


from fastapi import HTTPException

from fastapi import HTTPException, status

from app.core.uow import UnitOfWork
from app.detallepedido.schema import DetallePedidoCreate, DetallePedidoList, DetallePedidoPublic


class DetallePedidoService:

    def crear_detalle_pedido(self, detalle_pedido: DetallePedidoCreate
                            ) -> DetallePedidoPublic:
        with UnitOfWork() as uow:
            
            existe_producto = uow.productos.get_by_id(detalle_pedido.producto_id)
            if not existe_producto:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Producto no encontrado"
                )
            existe_pedido = uow.pedidos.get_by_id(detalle_pedido.pedido_id)
            if not existe_pedido:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Pedido no encontrado"
                )
            
            cantidad_personalizaciones = len(detalle_pedido.personalizacion)

            if cantidad_personalizaciones > detalle_pedido.cantidad:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No puede haber más listas de personalización que productos solicitados",
                )

            if cantidad_personalizaciones < detalle_pedido.cantidad:
                faltantes = detalle_pedido.cantidad - cantidad_personalizaciones

                detalle_pedido.personalizacion.extend(
                    [[] for _ in range(faltantes)]
                )
            nuevo_detalle = uow.detalles_pedido.create(detalle_pedido)
            return DetallePedidoPublic.model_validate(nuevo_detalle)
    
    def obtener_detalles_del_pedido(self, pedido_id: int)-> DetallePedidoList:

        with UnitOfWork() as uow:
            existe_pedido = uow.pedidos.get_by_id(pedido_id)
            if not existe_pedido:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Pedido no encontrado"
                )
            detalle_list = uow.detalles_pedido.get_by_id_pedido(pedido_id)
            return DetallePedidoList(
                data=[
                    DetallePedidoPublic.model_validate(detalle)
                    for detalle in detalle_list.data
                        ],
                count=len(detalle_list.data),
            )
            
    def obtener_detalle_por_id(self, pedido_id: int, producto_id: int) -> DetallePedidoPublic:
        with UnitOfWork() as uow:
            detalle = uow.detalles_pedido.get_by_id(pedido_id, producto_id)
            if not detalle:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Detalle de pedido no encontrado"
                )
            return DetallePedidoPublic.model_validate(detalle)
        
    
service = DetallePedidoService()