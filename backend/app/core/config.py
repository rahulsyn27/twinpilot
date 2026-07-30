from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Global application settings.

    Values are loaded from:
    1. Environment variables
    2. .env file
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # -------------------------------------------------------------------------
    # Application
    # -------------------------------------------------------------------------
    APP_NAME: str = "TwinPilot"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = "Your AI Engineering Twin"

    ENVIRONMENT: Literal["development", "staging", "production"] = "development"

    DEBUG: bool = True

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    API_V1_PREFIX: str = "/api/v1"

    # -------------------------------------------------------------------------
    # Security
    # -------------------------------------------------------------------------
    SECRET_KEY: str = Field(
        default="change-this-secret-key",
        description="Application secret key",
    )

    # -------------------------------------------------------------------------
    # PostgreSQL
    # -------------------------------------------------------------------------
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "twinpilot"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"

    # @property
    # def DATABASE_URL(self) -> str:
    #     return (
    #         f"postgresql+asyncpg://"
    #         f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
    #         f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/"
    #         f"{self.POSTGRES_DB}"
    #     ) #If the host changes, postgres to db.company.internal the URL updates automatically.
    
    @property
    def ASYNC_DATABASE_URL(self) -> str:
        """
        Used by the FastAPI application.
        """
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )

    @property
    def SYNC_DATABASE_URL(self) -> str:
        """
        Used only by Alembic migrations.
        """
        return (
            f"postgresql+psycopg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )
    # -------------------------------------------------------------------------
    # Redis
    # -------------------------------------------------------------------------
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    # -------------------------------------------------------------------------
    # Qdrant
    # -------------------------------------------------------------------------
    QDRANT_HOST: str = "qdrant"
    QDRANT_PORT: int = 6333

    @property
    def QDRANT_URL(self) -> str:
        return f"http://{self.QDRANT_HOST}:{self.QDRANT_PORT}"

    # -------------------------------------------------------------------------
    # LLM
    # -------------------------------------------------------------------------
    OPENAI_API_KEY: str = ""

    DEFAULT_MODEL: str = "gpt-4.1"

    # -------------------------------------------------------------------------
    # GitHub
    # -------------------------------------------------------------------------
    GITHUB_TOKEN: str = ""

    # -------------------------------------------------------------------------
    # Repository
    # -------------------------------------------------------------------------
    WORKSPACE_DIR: str = "./workspace"

    # -------------------------------------------------------------------------
    # Logging
    # -------------------------------------------------------------------------
    LOG_LEVEL: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "INFO"


@lru_cache  # Without caching, every request re-reads .env to instantiate Settings (slower); with caching, Settings is loaded once on the first request and reused for all subsequent requests.
def get_settings() -> Settings:
    """
    Cached settings instance.

    This ensures the configuration is loaded only once
    during the application's lifetime.
    """
    return Settings()


settings = get_settings()