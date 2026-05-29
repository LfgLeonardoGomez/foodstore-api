
from sqlmodel import select

from app.detallepedido.model import DetallePedido
from app.detallepedido.schema import DetallePedidoCreate, DetallePedidoList, DetallePedidoPublic


class DetallePedidoRepository: 
    def __init__(self, session):
        self.session = session

    def create(self, detalle_data: dict) -> DetallePedidoPublic:
        detalle_db = DetallePedido(**detalle_data)
        
        self.session.add(detalle_db)
        self.session.flush()
        self.session.refresh(detalle_db)
        return DetallePedidoPublic.model_validate(detalle_db)
    
    def get_by_id_pedido(self, pedido_id: int) -> DetallePedidoList:
        
        detalles = self.session.query(DetallePedido).filter(
            DetallePedido.pedido_id == pedido_id
        ).all()
        detalle_list = [DetallePedidoPublic.model_validate(d) for d in detalles]
        return DetallePedidoList(data=detalle_list, count=len(detalle_list))
    
    def get_by_id(self, pedido_id:int, producto_id:int) -> DetallePedidoPublic | None:
        detalle = self.session.query(DetallePedido).filter(
            DetallePedido.pedido_id == pedido_id,
            DetallePedido.producto_id == producto_id
        ).first()
        if not detalle:
            return None
            
        return DetallePedidoPublic.model_validate(detalle)
        
    
    