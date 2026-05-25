
from fastapi import FastAPI
from app.categoria.router import router as categoria_router
from app.producto.router import router as producto_router
from app.ingrediente.router import router as ingrediente_router
from app.usuarios.router import router as usuario_router
from app.direccioentrega.router import router as direccionentrega_router
from app.historialestadopedido.router import router as historial_estado_pedido_router
from app.detallepedido.router import router as detalle_pedido_router
from app.pedido.router import router as pedido_router
from app.core.database import create_db_and_tables
from app.core.seed import seed_data
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from seed import seed_productos


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    seed_data()
    # seed_productos()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categoria_router)
app.include_router(producto_router)
app.include_router(ingrediente_router)
app.include_router(usuario_router)
app.include_router(direccionentrega_router)
app.include_router(historial_estado_pedido_router)
app.include_router(detalle_pedido_router)
app.include_router(pedido_router)