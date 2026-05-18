# Gestión de Reservas de Discoteca — Backend

API RESTful para la gestión de reservas en discotecas, construida con **FastAPI** y **PostgreSQL (Neon)**.

## Características

- API RESTful con FastAPI
- Autenticación JWT (Bearer token)
- PostgreSQL en producción (Neon), SQLite en tests
- Alembic para migraciones
- 22 tablas en 5 esquemas (catalog, core, transactions, audit, system)
- 108 tests automatizados
- CI/CD con GitHub Actions (ruff + pytest)
- Ruff como linter/formatter

## Stack

| Capa       | Tecnología                         |
| ---------- | ---------------------------------- |
| Framework  | FastAPI 0.109                      |
| ORM        | SQLAlchemy 2.0                     |
| DB (prod)  | PostgreSQL 16 (Neon)               |
| DB (test)  | SQLite                             |
| Migraciones| Alembic 1.13                       |
| Auth       | JWT (python-jose + passlib/bcrypt) |
| Linter     | Ruff 0.3                           |
| Tests      | pytest 7.4 + pytest-cov            |
| CI/CD      | GitHub Actions                     |

## Requisitos

- Python 3.11+
- PostgreSQL 12+ (solo para desarrollo local)

## Instalación

```bash
git clone https://github.com/bxZknith85/gestion-reservas-discoteca-backend.git
cd gestion-reservas-discoteca-backend

python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/Mac

pip install -r requirements.txt
```

## Configuración

Copia `.env.example` a `.env` y edita:

```env
DATABASE_URL=postgresql+psycopg://user:password@host:5432/neondb?sslmode=require
SECRET_KEY=your-secret-key
DEBUG=True
ENVIRONMENT=development
ACCESS_TOKEN_EXPIRE_MINUTES=30
API_V1_STR=/api/v1
PROJECT_NAME="Gestión de Reservas - Discoteca"
```

## Ejecutar

```bash
uvicorn app.main:app --reload
```

Documentación interactiva en `http://localhost:8000/docs`.

## Tests

```bash
pytest                       # 108 tests
pytest -q --tb=line          # modo compacto
pytest --cov=app             # con cobertura
```

Los tests usan SQLite (`test.db`) que se regenera automáticamente al iniciar.

## Migraciones

```bash
alembic revision --autogenerate -m "descripcion"
alembic upgrade head
```

## Estructura del proyecto

```
app/
├── api/v1/endpoints/     # auth, events, orders, order_details,
│                         # reservations, tables, table_prices,
│                         # tickets, type_tickets, users
├── core/                 # config, security
├── crud/                 # lógica de acceso a datos
├── db/                   # database (engine, session)
├── models/               # catalog, core, transactions, audit, system
├── schemas/              # pydantic models
└── main.py

tests/                    # 9 archivos, 108 tests
migrations/versions/      # migraciones Alembic
.github/workflows/        # CI (ruff + pytest)
```

## Endpoints

### Auth
| Método | Ruta                  | Auth | Descripción         |
| ------ | --------------------- | ---- | ------------------- |
| POST   | `/api/v1/auth/login`  | No   | Iniciar sesión      |

### Usuarios
| Método | Ruta                        | Auth | Descripción            |
| ------ | ----------------------------| ---- | ---------------------- |
| POST   | `/api/v1/users/`            | No   | Registrar usuario      |
| GET    | `/api/v1/users/me`          | Sí   | Perfil actual          |
| GET    | `/api/v1/users/{id}`        | Sí   | Obtener usuario        |
| GET    | `/api/v1/users/`            | Sí   | Listar usuarios        |
| PUT    | `/api/v1/users/{id}`        | Sí   | Actualizar usuario     |
| DELETE | `/api/v1/users/{id}`        | Sí   | Eliminar usuario       |

### Eventos
| Método | Ruta                        | Auth | Descripción            |
| ------ | ----------------------------| ---- | ---------------------- |
| GET    | `/api/v1/events/`           | No   | Listar eventos         |
| GET    | `/api/v1/events/{id}`       | No   | Obtener evento         |
| POST   | `/api/v1/events/`           | Sí   | Crear evento           |
| PUT    | `/api/v1/events/{id}`       | Sí   | Actualizar evento      |
| DELETE | `/api/v1/events/{id}`       | Sí   | Eliminar evento        |

### Mesas
| Método | Ruta                        | Auth | Descripción            |
| ------ | ----------------------------| ---- | ---------------------- |
| GET    | `/api/v1/tables/`           | Sí   | Listar mesas           |
| GET    | `/api/v1/tables/{id}`       | Sí   | Obtener mesa           |
| POST   | `/api/v1/tables/`           | Sí   | Crear mesa             |
| PUT    | `/api/v1/tables/{id}`       | Sí   | Actualizar mesa        |
| DELETE | `/api/v1/tables/{id}`       | Sí   | Eliminar mesa          |

### Precios de mesa
| Método | Ruta                               | Auth | Descripción                  |
| ------ | -----------------------------------| ---- | ---------------------------- |
| GET    | `/api/v1/table-prices/`            | Sí   | Listar precios               |
| GET    | `/api/v1/table-prices/{id}`        | Sí   | Obtener precio               |
| GET    | `/api/v1/table-prices/event/{id}`  | Sí   | Precios por evento           |
| GET    | `/api/v1/table-prices/table/{id}`  | Sí   | Precios por mesa             |
| POST   | `/api/v1/table-prices/`            | Sí   | Crear precio                 |
| PUT    | `/api/v1/table-prices/{id}`        | Sí   | Actualizar precio            |
| DELETE | `/api/v1/table-prices/{id}`        | Sí   | Eliminar precio              |

### Tipos de ticket
| Método | Ruta                               | Auth | Descripción                  |
| ------ | -----------------------------------| ---- | ---------------------------- |
| GET    | `/api/v1/type-tickets/`            | Sí   | Listar tipos                 |
| GET    | `/api/v1/type-tickets/{id}`        | Sí   | Obtener tipo                 |
| GET    | `/api/v1/type-tickets/event/{id}`  | Sí   | Tipos por evento             |
| POST   | `/api/v1/type-tickets/`            | Sí   | Crear tipo                   |
| PUT    | `/api/v1/type-tickets/{id}`        | Sí   | Actualizar tipo              |
| DELETE | `/api/v1/type-tickets/{id}`        | Sí   | Eliminar tipo                |

### Reservas
| Método | Ruta                               | Auth | Descripción                  |
| ------ | -----------------------------------| ---- | ---------------------------- |
| GET    | `/api/v1/reservations/`            | Sí   | Listar reservas              |
| GET    | `/api/v1/reservations/{id}`        | Sí   | Obtener reserva              |
| GET    | `/api/v1/reservations/user/{id}`   | Sí   | Reservas de usuario          |
| POST   | `/api/v1/reservations/`            | Sí   | Crear reserva                |
| PUT    | `/api/v1/reservations/{id}`        | Sí   | Actualizar reserva           |
| DELETE | `/api/v1/reservations/{id}`        | Sí   | Eliminar reserva             |

### Tickets
| Método | Ruta                        | Auth | Descripción            |
| ------ | ----------------------------| ---- | ---------------------- |
| GET    | `/api/v1/tickets/`          | Sí   | Listar tickets         |
| GET    | `/api/v1/tickets/{id}`      | Sí   | Obtener ticket         |
| GET    | `/api/v1/tickets/user/{id}` | Sí   | Tickets de usuario     |
| POST   | `/api/v1/tickets/`          | Sí   | Crear ticket           |
| PUT    | `/api/v1/tickets/{id}`      | Sí   | Actualizar ticket      |
| DELETE | `/api/v1/tickets/{id}`      | Sí   | Eliminar ticket        |

### Órdenes
| Método | Ruta                               | Auth | Descripción                  |
| ------ | -----------------------------------| ---- | ---------------------------- |
| GET    | `/api/v1/orders/`                  | Sí   | Listar órdenes               |
| GET    | `/api/v1/orders/{id}`              | Sí   | Obtener orden                |
| GET    | `/api/v1/orders/user/{id}`         | Sí   | Órdenes de usuario           |
| POST   | `/api/v1/orders/`                  | Sí   | Crear orden                  |
| PUT    | `/api/v1/orders/{id}`              | Sí   | Actualizar orden             |
| DELETE | `/api/v1/orders/{id}`              | Sí   | Eliminar orden               |
| POST   | `/api/v1/orders/{id}/payments/`    | Sí   | Crear pago                   |
| GET    | `/api/v1/orders/{id}/payments/`    | Sí   | Listar pagos de orden        |
| PUT    | `/api/v1/orders/payments/{id}`     | Sí   | Actualizar pago              |

### Detalles de orden
| Método | Ruta                               | Auth | Descripción                  |
| ------ | -----------------------------------| ---- | ---------------------------- |
| GET    | `/api/v1/order-details/`           | Sí   | Listar detalles              |
| GET    | `/api/v1/order-details/{id}`       | Sí   | Obtener detalle              |
| GET    | `/api/v1/order-details/order/{id}` | Sí   | Detalles por orden           |
| POST   | `/api/v1/order-details/`           | Sí   | Crear detalle                |
| PUT    | `/api/v1/order-details/{id}`       | Sí   | Actualizar detalle           |
| DELETE | `/api/v1/order-details/{id}`       | Sí   | Eliminar detalle             |

### Health
| Método | Ruta                 | Auth | Descripción     |
| ------ | -------------------- | ---- | --------------- |
| GET    | `/health`            | No   | Health check    |
| GET    | `/api/v1/health`     | No   | API health      |

## Licencia

MIT — Ver archivo `LICENSE`.

## Autor

- GitHub: [@bxZknith85](https://github.com/bxZknith85)
