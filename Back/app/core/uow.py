from sqlmodel import Session
from app.core.database import get_engine
from app.categoria.repository import CategoriaRepository
from app.detallepedido.repository import DetallePedidoRepository
from app.direccioentrega.repository import DireccionEntregaRepository
from app.ingrediente.repository import IngredienteRepository
from app.producto.repository import ProductoRepository
from app.rol.repository import RolRepository
from app.usuarios.repository import UsuarioRepository

class UnitOfWork:
    def __init__(self):
        engine = get_engine()
        self.session: Session = Session(engine)

    def __enter__(self) -> "UnitOfWork":
        self.categorias = CategoriaRepository(self.session)
        self.productos = ProductoRepository(self.session)
        self.ingredientes = IngredienteRepository(self.session)
        self.usuarios = UsuarioRepository(self.session)
        self.direcciones = DireccionEntregaRepository(self.session)
        self.roles = RolRepository(self.session)
        self.detalles_pedido = DetallePedidoRepository(self.session)
        # Aquí irían más repositorios: self.productos = ProductoRepository(...)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

def get_uow() -> UnitOfWork:
    """Dependencia para obtener una instancia de UnitOfWork."""
    with UnitOfWork() as uow:
        yield uow