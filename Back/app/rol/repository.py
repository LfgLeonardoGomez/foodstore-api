
from sqlmodel import Session, select

from app.rol.model import Rol


class RolRepository: 
    def __init__(self, session: Session):
        self.session = session

    def get_by_codigo(self, codigo: str)-> Rol:
        statement = select(Rol).where(Rol.codigo==codigo)
        return self.session.exec(statement).first()
    
    def get_all(self) -> list[Rol]:
        statement = select(Rol.codigo)
        return self.session.exec(statement)
    
    