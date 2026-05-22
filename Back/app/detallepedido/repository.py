
from select import select

from app.detallepedido.model import DetallePedido
from app.detallepedido.schema import DetallePedidoCreate, DetallePedidoList, DetallePedidoPublic


class DetallePedidoRepository: 
    def __init__(self, session):
        self.session = session

    def create(self, detalle_pedido: DetallePedidoCreate
            )-> DetallePedidoPublic:
        detalle_db = DetallePedido.model_validate(detalle_pedido)
        
        self.session.add(detalle_db)
        self.session.flush()
        self.session.refresh(detalle_db)
        return DetallePedidoPublic.model_validate(detalle_db)
    
    def get_by_id_pedido(self, pedido_id: int) -> DetallePedidoList:
        
        statement = select(DetallePedido).where(
            DetallePedido.pedido_id == pedido_id)
        detalles = self.session.exec(statement).all()
        return DetallePedidoList(data=detalles, count=len(detalles))
    
    def get_by_id(self, pedido_id:int, producto_id:int) -> DetallePedidoPublic | None:
        statement = select(DetallePedido).where(
            DetallePedido.pedido_id == pedido_id,
            DetallePedido.producto_id == producto_id
        )
        detalle = self.session.exec(statement).first()
        if not detalle:
            return None
            
        return DetallePedidoPublic.model_validate(detalle)
        
    
    