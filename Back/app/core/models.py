from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB


from app.core.audit import AuditMixin

class ProductoCategoria(SQLModel, table=True):
    """Tabla intermedia para la relación muchos a muchos entre Productos y Categorías"""
    __tablename__ = "productos_categorias"
    
    producto_id: int = Field(foreign_key="productos.id", primary_key=True)
    categoria_id: int = Field(foreign_key="categorias.id", primary_key=True)


class ProductoIngrediente(SQLModel, table=True):
    """Tabla intermedia para la relación muchos a muchos entre Productos e Ingredientes"""
    __tablename__ = "productos_ingredientes"
    
    producto_id: int = Field(foreign_key="productos.id", primary_key=True)
    ingrediente_id: int = Field(foreign_key="ingredientes.id", primary_key=True)


class UsuarioRol(AuditMixin, SQLModel, table=True):
    __tablename__ = "usuario_rol"
    usuario_id : int = Field (foreign_key="usuarios.id", primary_key=True)
    rol_codigo : str = Field (foreign_key="roles.codigo", primary_key=True)

    asignado_por_id : int = Field(foreign_key="usuarios.id", nullable=True)

    # expires_at : datetime = Field (nullable=False)
    
