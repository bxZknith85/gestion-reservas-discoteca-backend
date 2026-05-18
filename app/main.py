from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import DataError, IntegrityError

from app.api.v1.endpoints import (
    events_router,
    order_details_router,
    orders_router,
    reservations_router,
    table_prices_router,
    tables_router,
    tickets_router,
    type_tickets_router,
    users_router,
)
from app.core.config import settings

# Importar todos los modelos para que SQLAlchemy los registre

# Nota: Las tablas ya existen en Supabase (ejecutadas desde schema_db.sql)
# No crear tablas automáticamente al startup con NullPool
# Base.metadata.create_all(bind=engine)

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


# --- Global exception handlers ---


@app.exception_handler(IntegrityError)
async def integrity_error_handler(_request: Request, exc: IntegrityError):
    """Captura violaciones de integridad (unique, FK, CHECK) y devuelve 409."""
    return JSONResponse(
        status_code=409,
        content={
            "detail": "Conflicto: la operación viola una restricción de integridad en la base de datos.",
            "error": str(exc.orig) if exc.orig else str(exc),
        },
    )


@app.exception_handler(DataError)
async def data_error_handler(_request: Request, exc: DataError):
    """Captura errores de datos (valor fuera de rango, tipo inválido) y devuelve 422."""
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Dato inválido para la base de datos.",
            "error": str(exc.orig) if exc.orig else str(exc),
        },
    )


@app.exception_handler(Exception)
async def global_exception_handler(_request: Request, exc: Exception):
    """Captura cualquier otra excepción no manejada y devuelve 500."""
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Error interno del servidor.",
            "error": str(exc),
        },
    )


# Incluir routers
app.include_router(users_router, prefix=settings.API_V1_STR)
app.include_router(events_router, prefix=settings.API_V1_STR)
app.include_router(tables_router, prefix=settings.API_V1_STR)
app.include_router(type_tickets_router, prefix=settings.API_V1_STR)
app.include_router(table_prices_router, prefix=settings.API_V1_STR)
app.include_router(reservations_router, prefix=settings.API_V1_STR)
app.include_router(tickets_router, prefix=settings.API_V1_STR)
app.include_router(orders_router, prefix=settings.API_V1_STR)
app.include_router(order_details_router, prefix=settings.API_V1_STR)


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
