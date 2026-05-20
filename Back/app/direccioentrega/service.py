

from fastapi import HTTPException, status

from app.core.uow import UnitOfWork
from app.direccioentrega.model import DireccionEntrega
from app.direccioentrega.schema import DireccionEntregaCreate, DireccionEntregaRead


class DireccionEntregaService:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def crear_direccion(direccion: DireccionEntregaCreate):
        with UnitOfWork() as uow: 
            if uow.direcciones.get_by_alias(direccion.alias):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                    detail="este alias ya existe")
            
            if not uow.usuarios.get_by_id(direccion.usuario_id):
                raise HTTPException(status_code=status.HTTP_404_BAD_REQUEST,
                                    detail=f"no existe el usuario con el id {direccion.usuario_id}")
            
            direccion_db = DireccionEntrega(**direccion.model_dump())
            uow.direcciones.create(direccion_db)
            return DireccionEntregaRead.model_validate(direccion_db)

    def listar_direcciones(offset: int = 0, limit: int = 10):
        with UnitOfWork() as uow:
            direcciones_db = uow.direcciones.get_all()
            data = [DireccionEntrega.model_validate(dir) for dir in direcciones_db]
            return data
        
    def get_by_id(direccion_id: int):
        pass

    def get_by_alias(alias: str):
        pass

    def actualizar_direccion(direccion_id: int, direccion: DireccionEntregaCreate):
        pass
    

direccionEntrega_service = DireccionEntregaService()