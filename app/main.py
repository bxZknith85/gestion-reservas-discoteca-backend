from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.database import Base, engine
from app.api.v1.endpoints import (
    reservas_router,
    usuarios_router,
    eventos_router,
    salas_router,
)

# Crear tablas
Base.metadata.create_all(bind=engine)

# Crear aplicación
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
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
app.include_router(usuarios_router, prefix=settings.API_V1_STR)
app.include_router(salas_router, prefix=settings.API_V1_STR)
app.include_router(eventos_router, prefix=settings.API_V1_STR)
app.include_router(reservas_router, prefix=settings.API_V1_STR)


@app.get("/")
def read_root():
    """Health check endpoint"""
    return {
        "message": "Gestión de Reservas de Discoteca - Backend",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
    }


@app.get("/api/v1/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
