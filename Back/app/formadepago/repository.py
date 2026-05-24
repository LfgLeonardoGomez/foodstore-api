

from sqlmodel import Session, select

from app.formadepago.model import FormaDePago


class FormaDePagoRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all_formas_de_pago(self):
        statement = select(FormaDePago)
        return self.session.exec(statement).all()
    
    def get_forma_de_pago_by_codigo(self, codigo: str):
        statement = select(FormaDePago).where(FormaDePago.codigo == codigo)
        return self.session.exec(statement).first()
    
