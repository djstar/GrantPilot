"""
GrantPilot Configuration
Uses Pydantic Settings for environment variable management
"""

from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    app_name: str = "GrantPilot"
    environment: str = "development"
    debug: bool = True

    # Database
    database_url: str = "postgresql://grantpilot:grantpilot_dev@localhost:5432/grantpilot"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # LLM API Keys
    anthropic_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None

    # File Storage
    upload_dir: str = "/app/uploads"
    max_upload_size_mb: int = 50

    # Security
    secret_key: str = "dev-secret-key-change-in-production"

    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    @property
    def async_database_url(self) -> str:
        """Convert sync URL to async for asyncpg"""
        return self.database_url.replace("postgresql://", "postgresql+asyncpg://")


@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance"""
    return Settings()
