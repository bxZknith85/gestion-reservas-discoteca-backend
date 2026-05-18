import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuración de la aplicación"""

    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Gestión de Reservas de Discoteca"
    PROJECT_DESCRIPTION: str = "Sistema backend para gestión de reservas en discotecas"
    VERSION: str = "1.0.0"

    # Database - PostgreSQL (Neon)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:password@localhost:5432/postgres")

    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS — se parsea automáticamente desde JSON string en .env
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Environment
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
