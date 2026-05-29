



from decimal import Decimal

from fastapi import HTTPException, status

from app.core.uow import UnitOfWork
from app.historialestadopedido.model import HistorialEstadoPedido
from app.pedido.schema import PedidoCreate, PedidoList, PedidoPublic, PedidoRead
from app.usuarios.model import Usuario


class PedidoService:



    def crear_pedido(self,usuario_id: int, pedido: PedidoCreate) -> PedidoRead:
        with UnitOfWork() as uow:

            existeusuario = uow.usuarios.get_by_id(usuario_id)
            if not existeusuario:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado",
                )
            
            existedireccion = uow.direcciones.get_by_id(pedido.direccion_id)
            if not existedireccion:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Direccion no encontrada",
                )
            if existedireccion.usuario_id != usuario_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La dirección no pertenece al usuario.",
                )
            existe_forma_pago = uow.formas_pago.get_forma_de_pago_by_codigo(pedido.forma_pago_codigo)
            
            if not existe_forma_pago:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Forma de pago no válida.",
                )
            
            if not pedido.detalles:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El pedido debe tener al menos un detalle.",
                )
            #      Creo el pedido primero para obtener el id
            pedido_db = uow.pedidos.create({
                "direccion_id": pedido.direccion_id,
                "forma_pago_codigo": pedido.forma_pago_codigo,
                "descuento": pedido.descuento,
                "notas": pedido.notas,
                "usuario_id": usuario_id,
                "estado_codigo": "PENDIENTE",
                "subtotal": Decimal("0"),
                "total": Decimal("0"),
                "costo_envio": Decimal("50.00"),
            })

            for detalle in pedido.detalles:
                detalle_data = detalle.model_dump()
                detalle_data["pedido_id"] = pedido_db.id
                detalle_data["subtotal_snapshot"] = detalle_data["precio_snapshot"] * detalle_data["cantidad"]
                uow.detalles_pedido.create(detalle_data)

            #        Traigo de nuevo el pedido para actualizar los detalles
            pedido_db = uow.pedidos.get_by_id(pedido_db.id) 

            subtotal_pedido = sum(d.precio_snapshot * d.cantidad for d in pedido_db.detalles)
            total_pedido = Decimal(str(subtotal_pedido)) + pedido_db.costo_envio - pedido_db.descuento

            pedido_db.subtotal = subtotal_pedido
            pedido_db.total = total_pedido

            rta= uow.pedidos.update(pedido_db)

            uow.historialestadopedido.create(
            
            HistorialEstadoPedido(
            pedido_id=pedido_db.id,
            estado_desde=None,       # RN-02 — primera transición
            estado_hacia="PENDIENTE",
            usuario_id=usuario_id,
            motivo=None
            )
)

            return PedidoRead.model_validate(rta)
        
        #  traer los pedidos de un cliente,

    def traer_pedidos_por_cliente(self, cliente_id: int) -> PedidoList:
        with UnitOfWork() as uow:
            existecliente = uow.usuarios.get_by_id(cliente_id)
            if not existecliente:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado",
                )
            
            data = uow.pedidos.get_by_usuario_id(cliente_id)
            count = len(data)

            return PedidoList(data=[PedidoPublic.model_validate(p) for p in data], count=count)
        
        
        #  traer todos los pedidos

    def traer_todos_los_pedidos(self) -> PedidoList:
        with UnitOfWork() as uow:
            data = uow.pedidos.get_all()
            count = len(data)

            return PedidoList(data=[PedidoPublic.model_validate(p) for p in data], count=count)

        #  traer pedidos por estado

    def traer_pedidos_por_estado(self, estado_codigo: str) -> PedidoList:
        with UnitOfWork() as uow:
            existeestado = uow.estadopedido.get_by_codigo(estado_codigo)
            if not existeestado:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Estado de pedido no encontrado",
                )
            data = uow.pedidos.get_by_estado(estado_codigo)
            count = len(data)

            return PedidoList(data=[PedidoPublic.model_validate(p) for p in data], count=count)
    
        #  traer pedidos de un cliente por estado,

    def traer_pedidos_por_estado_por_cliente(self, cliente_id: int, estado_codigo: str) -> PedidoList:
        with UnitOfWork() as uow:
            existecliente = uow.usuarios.get_by_id(cliente_id)
            if not existecliente:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado",
                )
            existeestado = uow.estadopedido.get_by_codigo(estado_codigo)
            if not existeestado:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Estado de pedido no encontrado",
                )
            data = uow.pedidos.get_by_estado_by_usuario_id(cliente_id, estado_codigo)
            count = len(data)

            return PedidoList(data=[PedidoPublic.model_validate(p) for p in data], count=count)


        #  traer un pedido por id. 

    def traer_pedido_por_id(self, pedido_id: int, usuario: Usuario) -> PedidoRead:
        with UnitOfWork() as uow:
            pedido = uow.pedidos.get_by_id(pedido_id)
            if not pedido:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Pedido no encontrado",
                )
            
            if not any(r.codigo in ["ADMIN", "PEDIDOS"] for r in usuario.roles) and pedido.usuario_id != usuario.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tenés permiso para ver este pedido.",
                )
        
            return PedidoRead.model_validate(pedido)
        
pedidoservice = PedidoService()