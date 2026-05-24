
from sqlmodel import Session, select

from app.estadopedido.model import EstadoPedido


class EstadoPedidoRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_by_codigo(self, codigo: str):
        statement = select(EstadoPedido).where(EstadoPedido.codigo==codigo)
        return self.session.exec(statement).first()
    
    def get_all(self) -> list[EstadoPedido]:
        statement = select(EstadoPedido)
        return self.session.exec(statement).all()