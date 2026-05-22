

from sqlmodel import Field, SQLModel


class FormaDePago(SQLModel, table = True):
    __tablename__ = "forma_de_pago"
    codigo : str = Field(primary_key = True, max_length = 20)
    descripcion : str = Field(max_length = 100, nullable=False)
    habilitado : bool = Field (default=True, nullable=False)