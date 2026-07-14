<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white" alt="JWT" />
</p>

# FoodStore — Backend API

**Trabajo Práctico — Programación 4**
**UTN — Facultad Regional Mendoza**

> Parte del proyecto FoodStore (TPI Programación 4).
> Repos relacionados: [Panel Admin](https://github.com/LfgLeonardoGomez/foodstore-admin) · [Tienda Cliente](https://github.com/LfgLeonardoGomez/foodstore-store-cliente)

---

## 🎥 Video de presentación

El video muestra el flujo completo de la tienda de punta a punta, desde la perspectiva del cliente: login y registro, catálogo con filtros, carrito con validación de stock en tiempo real, checkout con pago vía MercadoPago, y perfil de usuario con historial de pedidos y direcciones de entrega.

<a href="https://youtu.be/SkHezWvJIcg" target="_blank">
  <img src="https://img.youtube.com/vi/SkHezWvJIcg/maxresdefault.jpg" alt="Ver video de presentación de FoodStore" width="100%" />
</a>

**[▶ Ver en YouTube](https://youtu.be/SkHezWvJIcg)**

---

## Integrantes

| Nombre   | Apellido |
| -------- | -------- |
| Leonardo | Gómez    |
| Nicolás  | Castro   |

---

## Descripción del Proyecto

Este repositorio contiene el **backend** de **FoodStore**, una aplicación fullstack de pedidos de comida. La API expone endpoints RESTful para gestionar el catálogo de productos, usuarios, pedidos, direcciones de entrega, pagos y más.

El servidor se encarga de:

- Exponer una API REST segura con autenticación JWT y RBAC (4 roles)
- Gestionar la persistencia de datos con PostgreSQL a través de SQLModel
- Notificar cambios de estado de pedidos en tiempo real vía WebSocket
- Procesar pagos con MercadoPago Checkout PRO
- Gestionar imágenes de productos y categorías en Cloudinary
- Precargar datos iniciales automáticamente al iniciar (seed integrado)
- Aplicar rate limiting en endpoints de autenticación

## Funcionalidades destacadas

- **Máquina de estados de pedidos**: cada pedido transiciona por estados válidos y controlados (ej. pendiente → confirmado → en preparación → entregado), evitando transiciones inconsistentes.
- **Unit of Work**: las operaciones que tocan múltiples tablas (ej. crear un pedido y descontar stock) se ejecutan de forma atómica, con rollback automático ante errores.
- **JWT en cookies HttpOnly**: los tokens de acceso no quedan expuestos a JavaScript en el cliente, mitigando ataques XSS.
- **RBAC de 4 roles** (Admin, Stock, Pedidos, Cliente), con permisos diferenciados a nivel de endpoint.

---

## Tecnologías

| Tecnología           | Uso                                                |
| -------------------- | -------------------------------------------------- |
| **Python 3**         | Lenguaje principal                                 |
| **FastAPI**          | Framework web para APIs de alto rendimiento        |
| **SQLModel**         | ORM/Modelado de datos sobre SQLAlchemy             |
| **PostgreSQL**       | Base de datos relacional                           |
| **Uvicorn**          | Servidor ASGI para ejecutar la aplicación          |
| **Pydantic**         | Validación y serialización de datos                |
| **python-jose**      | Manejo de tokens JWT                               |
| **passlib + bcrypt** | Hashing seguro de contraseñas                      |
| **WebSocket**        | Notificaciones en tiempo real de estados de pedido |
| **Cloudinary**       | Almacenamiento y gestión de imágenes               |
| **MercadoPago**      | Pasarela de pagos (Checkout PRO)                   |
| **slowapi**          | Rate limiting en endpoints de autenticación        |
| **python-dotenv**    | Carga de variables de entorno desde `.env`         |
| **python-multipart** | Soporte para formularios multipart                 |

---

## Requisitos Previos

- Python 3.10+
- PostgreSQL 15+ corriendo localmente

---

## Instalación

1. **Crear y activar el entorno virtual:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. **Instalar dependencias:**

```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno:**

```bash
cp .env.example .env
```

Completar `.env` con las credenciales de base de datos, Cloudinary y MercadoPago.

---

## Levantar el Servidor

```bash
uvicorn app.main:app --reload
```

- **URL base:** `http://localhost:8000`
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

Las tablas y el seed se ejecutan automáticamente al iniciar.

---

## Credenciales seed

> Usuarios de prueba generados automáticamente al levantar el proyecto. Solo para entorno local/demo.

| Rol     | Email                   | Contraseña  |
| ------- | ----------------------- | ----------- |
| Admin   | admin@foodstore.com     | admin1234   |
| Stock   | stock@foodstore.com     | stock1234   |
| Pedidos | pedidos@foodstore.com   | pedidos1234 |

---

## Estructura de Módulos

```
app/
├── core/                # Configuración, BD, seed, UoW, WebSocket
├── modules/
│   ├── auth/            # Login, registro, refresh, logout
│   ├── usuarios/        # CRUD usuarios y roles
│   ├── categoria/       # Categorías de productos
│   ├── producto/        # Catálogo de productos
│   ├── ingrediente/     # Ingredientes
│   ├── pedido/          # Gestión de pedidos + WebSocket
│   ├── pago/            # Integración MercadoPago
│   ├── uploads/         # Upload/delete imágenes Cloudinary
│   └── direccioentrega/ # Direcciones de entrega
└── main.py              # Punto de entrada
```
