from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings supporting multiple databases."""
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    # Logging
    LOG_LEVEL: str
    ENVIRONMENT: str
    DEFAULT_COMPANY_SLUG: str
    
    # PostgreSQL (Primary Database)
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DATABASE: str
    POSTGRES_POOL_SIZE: int = 20
    POSTGRES_MAX_OVERFLOW: int = 0
    POSTGRES_ECHO: bool = False
    
    # Database URL Properties
    @property
    def postgres_async_url(self) -> str:
        """PostgreSQL async connection URL."""
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DATABASE}"
        )

settings = Settings()
