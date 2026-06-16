from sqlmodel import Session, select
from app.unidadMedida.model import UnidadMedida

class UnidadMedidaRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> list[UnidadMedida]:
        statement = select(UnidadMedida)
        return self.session.exec(statement).all()
    
    def get_by_id(self, id: int) -> UnidadMedida | None:
        statement = select(UnidadMedida).where(UnidadMedida.id == id)
        return self.session.exec(statement).first()
    
    def get_by_nombre(self, nombre: str) -> UnidadMedida | None:
        statement = select(UnidadMedida).where(UnidadMedida.nombre == nombre)
        return self.session.exec(statement).first()