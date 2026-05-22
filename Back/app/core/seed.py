from app.core.security import hash_password
from app.core.uow import UnitOfWork
from app.rol.model import Rol
from app.usuarios.model import Usuario


ROLES_BASE = [
    {
        "codigo": "ADMIN",
        "nombre": "Administrador",
        "descripcion": "Acceso completo al sistema",
    },
    {
        "codigo": "STOCK",
        "nombre": "Stock",
        "descripcion": "Gestión de productos, ingredientes y stock",
    },
    {
        "codigo": "PEDIDOS",
        "nombre": "Pedidos",
        "descripcion": "Gestión de pedidos del sistema",
    },
    {
        "codigo": "CLIENT",
        "nombre": "Cliente",
        "descripcion": "Usuario cliente del sistema",
    },
]


def seed_roles() -> None:
    with UnitOfWork() as uow:
        for rol_data in ROLES_BASE:
            rol_existente = uow.roles.get_by_codigo(rol_data["codigo"])

            if rol_existente:
                continue

            rol = Rol(
                codigo=rol_data["codigo"],
                nombre=rol_data["nombre"],
                descripcion=rol_data["descripcion"],
            )

            uow.session.add(rol)


def seed_admin() -> None:
    with UnitOfWork() as uow:
        admin_existente = uow.usuarios.get_by_email("admin@foodstore.com")

        if admin_existente:
            return

        rol_admin = uow.roles.get_by_codigo("ADMIN")

        if not rol_admin:
            raise RuntimeError("No existe el rol ADMIN. Ejecutá seed_roles primero.")

        admin = Usuario(
            nombre="Admin",
            apellido="Sistema",
            email="admin@foodstore.com",
            celular="0000000000",
            password_hashed=hash_password("admin1234"),
            disabled=False,
            roles=[rol_admin],
        )

        uow.session.add(admin)



        # Credenciales del admin:
        # email: admin@foodstore.com
        # password: admin1234

def seed_data() -> None:
    seed_roles()
    seed_admin()