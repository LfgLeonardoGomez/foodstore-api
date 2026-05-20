from sqlmodel import Session, select, update

from app.direccioentrega.model import DireccionEntrega
from app.direccioentrega.schema import DireccionEntregaCreate


class DireccionEntregaRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, direccion_id: int) -> DireccionEntrega:
        statement = select(DireccionEntrega).where(DireccionEntrega.id==direccion_id,
                                DireccionEntrega.disabled==False)
        return self.session.exec(statement).first()
    
    def get_by_alias(self, alias: str) -> DireccionEntrega:
        statement = select(DireccionEntrega).where(DireccionEntrega.alias==alias,
                                DireccionEntrega.disabled==False)
        return self.session.exec(statement).first()
    
    def get_all(self, offset: int = 0, limit: int = 10) -> list[DireccionEntrega]:
        statement = select(DireccionEntrega).where(DireccionEntrega.disabled==False)
        return self.session.exec(statement)
    
    def create(self, direccion: DireccionEntregaCreate) -> DireccionEntrega:
        self.session.add(direccion)
        self.session.flush()
        self.session.refresh(direccion)
        return direccion
    
    def update(self, direccion_id: int, direccion: DireccionEntregaCreate) -> None:
        direccion_db = self.get_by_id(direccion_id)
        if not direccion:
            raise ValueError(f"Direccion no encontrada para el id : {direccion_id}")
        
        direccion.disabled = True
        self.session.add(direccion)
        self.session.flush()
        self.session.refresh(direccion)
        return direccion
    
    def actualizar_principal(self, direccion_id: int) -> None:
        direccion = self.get_by_id(direccion_id)
        if not direccion:
            raise ValueError(f"Direccion no encontrada para el id : {direccion_id}")
        
        self.session.exec(update(DireccionEntrega).where(DireccionEntrega.usuario_id==direccion.usuario_id)
                        .values(es_principal=False))
        
        direccion.es_principal = True

        self.session.add(direccion)
        self.session.flush()
        self.session.refresh(direccion)

        return direccion
    
    def delete(self, direccion_id: DireccionEntrega) -> None:
        direccion = self.get_by_id(direccion_id)
        if not direccion:
            raise ValueError(f"Direccion no encontrada para el id : {direccion_id}")
        
        direccion.disabled = True
        self.session.add(direccion)
        self.session.flush()
        self.session.refresh(direccion)
