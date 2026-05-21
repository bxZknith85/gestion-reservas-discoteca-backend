# Gestión de Reservas - Discoteca

API REST para la gestión de reservas de mesas, venta de entradas y administración de discotecas.

## Stack

- Python 3.12, Django 6.0, Django REST Framework
- PostgreSQL 16 (5 esquemas: `catalog`, `core`, `transactions`, `audit`, `system`)
- JWT (`djangorestframework-simplejwt`)
- Docker + Render (gunicorn)

## Estructura

```
apps/
├── catalog/     # Tablas de referencia (TypeUser, EventState, PaymentMethod...)
├── core/        # User, Event, DicoTable, TypeTicket, TablePrice + auth
├── transactions/# Order, Reservation, Ticket, OrderDetail, Payment
├── audit/       # AuditLog
└── system/      # AdminActionLog, AppConfig
config/          # settings.py, urls.py, wsgi.py, asgi.py, test_settings.py
tests/           # 88 tests (pytest)
```

## Inicio rápido

```bash
python -m venv venv
venv\Scripts\activate    # Windows
pip install -r requirements.txt
cp .env.example .env     # configurar DB
python manage.py migrate
python manage.py runserver
```

## Docker

```bash
docker compose up --build
```

## Tests

```bash
pytest -v            # SQLite in-memory (test_settings.py)
pytest --cov=apps    # con cobertura
```

## API

| Endpoint | Métodos | Auth |
|---|---|---|
| `/api/v1/auth/login/` | POST | ❌ |
| `/api/v1/health/` | GET | ❌ |
| `/api/v1/users/` | GET, POST | registro público |
| `/api/v1/users/me/` | GET | JWT |
| `/api/v1/events/` | GET, POST, PUT, PATCH, DELETE | GET público |
| `/api/v1/tables/` | CRUD | JWT |
| `/api/v1/type-tickets/` | CRUD | JWT |
| `/api/v1/table-prices/` | CRUD | JWT |
| `/api/v1/orders/` | CRUD | JWT |
| `/api/v1/orders/{id}/payments/` | GET, POST | JWT |
| `/api/v1/reservations/` | CRUD | JWT |
| `/api/v1/tickets/` | CRUD | JWT |
| `/api/v1/order-details/` | CRUD | JWT |
| `/api/v1/payments/` | GET, PUT, PATCH | JWT |
| `/api/v1/audit-logs/` | GET | JWT |
| `/api/v1/admin-actions/` | GET | JWT |
| `/api/v1/app-config/` | GET | JWT |

## Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

Los datos de catálogo (TypeUser, EventState, etc.) y AppConfig se siembran automáticamente con `migrate`.

## Variables de entorno

Ver `.env.example` — `DATABASE_URL`, `SECRET_KEY`, `API_V1_STR`, CORS, etc.
