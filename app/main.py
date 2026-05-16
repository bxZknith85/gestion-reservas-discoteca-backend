from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.database import Base, engine
from app.api.v1.endpoints import (
    users_router,
    events_router,
    tables_router,
    reservations_router,
    orders_router,
)

# Importar todos los modelos para que SQLAlchemy los registre
from app.models import (
    TypeUser, EventState, ReservationState, TableState,
    TableType, TicketState, PaymentMethod, OrderStatus,
    User, Event, DicoTable, TypeTicket, TablePrice,
    Order, Reservation, Ticket, OrderDetail, Payment,
    AuditLog,
    AdminActionLog, AppConfig,
)

# Crear tablas (solo si no existen)
Base.metadata.create_all(bind=engine)

# Crear aplicación
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(users_router, prefix=settings.API_V1_STR)
app.include_router(events_router, prefix=settings.API_V1_STR)
app.include_router(tables_router, prefix=settings.API_V1_STR)
app.include_router(reservations_router, prefix=settings.API_V1_STR)
app.include_router(orders_router, prefix=settings.API_V1_STR)


@app.get("/")
def read_root():
    """Health check endpoint"""
    return {
        "message": "Gestión de Reservas de Discoteca - Backend API",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "docs": f"{settings.API_V1_STR}/docs",
    }


@app.get(f"{settings.API_V1_STR}/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
