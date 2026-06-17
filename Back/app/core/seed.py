from app.core.security import hash_password
from app.core.uow import UnitOfWork
from app.rol.model import Rol
from app.modules.usuarios.model import Usuario
from app.formadepago.model import FormaDePago
from app.estadopedido.model import EstadoPedido
from app.unidadMedida.model import UnidadMedida
from app.modules.categoria.model import Categoria
from app.modules.producto.model import Producto

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


FORMAS_PAGO_BASE = [
    {
        "codigo": "EFECTIVO",
        "nombre": "Efectivo",
        "descripcion": "Pago en efectivo contra entrega",
    },
    {
        "codigo": "MERCADOPAGO",
        "nombre": "MercadoPago",
        "descripcion": "Pago a través de MercadoPago",
    },
    {
        "codigo": "TRANSFERENCIA",
        "nombre": "Transferencia bancaria",
        "descripcion": "Transferencia bancaria directa",
    },
]


ESTADOS_PEDIDO_BASE = [
    {
        "codigo": "PENDIENTE",
        "descripcion": "Pedido recibido, esperando confirmación",
        "orden": 1,
        "es_terminal": False,
    },
    {
        "codigo": "CONFIRMADO",
        "descripcion": "Pedido confirmado, en preparación",
        "orden": 2,
        "es_terminal": False,
    },
    {
        "codigo": "EN_PREP",
        "descripcion": "Pedido en preparación en cocina",
        "orden": 3,
        "es_terminal": False,
    },
    {
        "codigo": "LISTO",
        "descripcion": "Pedido listo para retirar o entregar",
        "orden": 4,
        "es_terminal": False,
    },
    {
        "codigo": "ENTREGADO",
        "descripcion": "Pedido entregado exitosamente",
        "orden": 5,
        "es_terminal": True,
    },
    {
        "codigo": "CANCELADO",
        "descripcion": "Pedido cancelado",
        "orden": 6,
        "es_terminal": True,
    },
]

UNIDADES_MEDIDA_BASE = [
    {
        "nombre": "Kilogramo",
        "simbolo": "kg",
        "tipo": "peso",
    },
    {
        "nombre": "Gramo",
        "simbolo": "gr",
        "tipo": "peso",
    },
    {
        "nombre": "Litro",
        "simbolo": "lt",
        "tipo": "volumen",
    },
    {
        "nombre": "Mililitro",
        "simbolo": "ml",
        "tipo": "volumen",
    },
    {
        "nombre": "Unidad",
        "simbolo": "un",
        "tipo": "unidad",
    },
    {
        "nombre": "Docena",
        "simbolo": "doc",
        "tipo": "unidad",
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


def seed_formas_pago() -> None:
    with UnitOfWork() as uow:
        for fp_data in FORMAS_PAGO_BASE:
            fp_existente = uow.formas_pago.get_forma_de_pago_by_codigo(fp_data["codigo"])

            if fp_existente:
                continue

            fp = FormaDePago(
                codigo=fp_data["codigo"],
                nombre=fp_data["nombre"],
                descripcion=fp_data["descripcion"],
            )

            uow.session.add(fp)


def seed_estados_pedido() -> None:
    with UnitOfWork() as uow:
        for estado_data in ESTADOS_PEDIDO_BASE:
            estado_existente = uow.estadopedido.get_by_codigo(estado_data["codigo"])

            if estado_existente:
                continue

            estado = EstadoPedido(
                codigo=estado_data["codigo"],
                descripcion=estado_data["descripcion"],
                orden=estado_data["orden"],
                es_terminal=estado_data["es_terminal"],
            )

            uow.session.add(estado)

def seed_unidades_medida() -> None:
    with UnitOfWork() as uow:
        for um_data in UNIDADES_MEDIDA_BASE:
            um_existente = uow.unidades_medida.get_by_nombre(um_data["nombre"])
            if um_existente:
                continue

            um = UnidadMedida(
                nombre=um_data["nombre"],
                simbolo=um_data["simbolo"],
                tipo=um_data["tipo"],
            )
            uow.session.add(um)

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

def seed_test_users() -> None:
    with UnitOfWork() as uow:
        usuarios_test = [
            {
                "email": "stock@foodstore.com",
                "password": "stock1234",
                "nombre": "Juan",
                "apellido": "Stock",
                "rol": "STOCK"
            },
            {
                "email": "pedidos@foodstore.com",
                "password": "pedidos1234",
                "nombre": "Maria",
                "apellido": "Pedidos",
                "rol": "PEDIDOS"
            },
        ]

        for u in usuarios_test:
            if uow.usuarios.get_by_email(u["email"]):
                continue

            rol = uow.roles.get_by_codigo(u["rol"])
            nuevo = Usuario(
                nombre=u["nombre"],
                apellido=u["apellido"],
                email=u["email"],
                celular="0000000000",
                password_hashed=hash_password(u["password"]),
                disabled=False,
                roles=[rol],
            )
            uow.session.add(nuevo)


# ─── CATEGORÍAS ──────────────────────────────────────────────────────────────
# Imágenes de Unsplash (libres de uso, hotlinking permitido)

CATEGORIAS_BASE = [
    {
        "nombre": "Pizzas",
        "descripcion": "Pizzas artesanales al horno de barro",
        "imagen_url": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=600&q=80",
    },
    {
        "nombre": "Hamburguesas",
        "descripcion": "Hamburguesas gourmet con carne 100% vacuna",
        "imagen_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=600&q=80",
    },
    {
        "nombre": "Empanadas",
        "descripcion": "Empanadas criollas horneadas y fritas",
        "imagen_url": "https://images.unsplash.com/photo-1530469940413-339b7f070deb?w=600&q=80",
    },
    {
        "nombre": "Bebidas",
        "descripcion": "Gaseosas, jugos y bebidas sin alcohol",
        "imagen_url": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=600&q=80",
    },
]


def seed_categorias() -> None:
    with UnitOfWork() as uow:
        for cat_data in CATEGORIAS_BASE:
            if uow.categorias.get_by_nombre(cat_data["nombre"]):
                continue

            categoria = Categoria(
                nombre=cat_data["nombre"],
                descripcion=cat_data["descripcion"],
                disponible=True,
                imagen_url=cat_data["imagen_url"],
            )
            uow.session.add(categoria)


# ─── PRODUCTOS ───────────────────────────────────────────────────────────────
# Imágenes de Unsplash (libres de uso, hotlinking permitido)

PRODUCTOS_BASE = [
    {
        "nombre": "Pizza Mozzarella",
        "descripcion": "Salsa de tomate, mozzarella fresca y orégano",
        "precio_base": "12000.00",
        "stock_cantidad": 50,
        "imagen_url": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=600&q=80",
        "categorias": ["Pizzas"],
    },
    {
        "nombre": "Pizza Pepperoni",
        "descripcion": "Salsa de tomate, mozzarella y pepperoni extra",
        "precio_base": "14500.00",
        "stock_cantidad": 40,
        "imagen_url": "https://images.unsplash.com/photo-1628840042765-356cda07504e?w=600&q=80",
        "categorias": ["Pizzas"],
    },
    {
        "nombre": "Hamburguesa Clásica",
        "descripcion": "Carne 200g, lechuga, tomate, queso cheddar y mayonesa casera",
        "precio_base": "8500.00",
        "stock_cantidad": 60,
        "imagen_url": "https://images.unsplash.com/photo-1550547660-d9450f859349?w=600&q=80",
        "categorias": ["Hamburguesas"],
    },
    {
        "nombre": "Empanada de Carne",
        "descripcion": "Carne picada, cebolla, huevo duro y aceitunas",
        "precio_base": "1800.00",
        "stock_cantidad": 100,
        "imagen_url": "https://images.unsplash.com/photo-1600891964092-4316c288032e?w=600&q=80",
        "categorias": ["Empanadas"],
    },
    {
        "nombre": "Coca Cola 500ml",
        "descripcion": "Gaseosa Coca Cola individual 500ml",
        "precio_base": "2500.00",
        "stock_cantidad": 200,
        "imagen_url": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=600&q=80",
        "categorias": ["Bebidas"],
    },
]


def seed_productos() -> None:
    with UnitOfWork() as uow:
        for prod_data in PRODUCTOS_BASE:
            if uow.productos.get_by_nombre(prod_data["nombre"]):
                continue

            # Buscar las categorías por nombre
            categorias_obj = []
            for cat_nombre in prod_data["categorias"]:
                cat = uow.categorias.get_by_nombre(cat_nombre)
                if cat:
                    categorias_obj.append(cat)

            producto = Producto(
                nombre=prod_data["nombre"],
                descripcion=prod_data["descripcion"],
                precio_base=prod_data["precio_base"],
                stock_cantidad=prod_data["stock_cantidad"],
                disponible=True,
                imagen_url=prod_data["imagen_url"],
                categorias=categorias_obj,
            )
            uow.session.add(producto)


def seed_data() -> None:
    seed_roles()
    seed_formas_pago()
    seed_estados_pedido()
    seed_unidades_medida()
    seed_admin()
    seed_test_users()
    seed_categorias()
    seed_productos()