from sqlmodel import Session, select

from app.core.database import engine, get_engine
from app.rol.model import Rol


ROLES_INICIALES = [
    {
        "codigo": "ADMIN",
        "nombre": "admin",
        "descripcion": "Administrador del sistema"
    },
    {
        "codigo": "STOCK",
        "nombre": "stock",
        "descripcion": "Encargado del stock"
    },
    {
        "codigo": "PEDIDOS",
        "nombre": "pedidos",
        "descripcion": "Gestión de pedidos"
    },
    {
        "codigo": "CLIENTE",
        "nombre": "cliente",
        "descripcion": "Cliente de la aplicación"
    }
]

engine = get_engine()

def seed_roles():
    with Session(engine) as session:

        for rol_data in ROLES_INICIALES:

            # Verifica si ya existe
            rol_existente = session.exec(
                select(Rol).where(Rol.codigo == rol_data["codigo"])
            ).first()

            if rol_existente:
                print(f"El rol {rol_data['codigo']} ya existe")
                continue

            nuevo_rol = Rol(**rol_data)

            session.add(nuevo_rol)

        session.commit()

        print("Roles cargados correctamente")


if __name__ == "__main__":
    seed_roles()