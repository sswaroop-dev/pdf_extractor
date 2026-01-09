"""PostgreSQL database connection and session management."""

from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine, AsyncSession, create_async_engine
)
from sqlalchemy.orm import sessionmaker

from ...config import settings


# Create async engine
postgres_engine: AsyncEngine = create_async_engine(
    settings.postgres_async_url,
    pool_size=settings.POSTGRES_POOL_SIZE,
    max_overflow=settings.POSTGRES_MAX_OVERFLOW,
    echo=settings.POSTGRES_ECHO,
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    bind=postgres_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Dependency function for FastAPI
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency for getting database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def check_db():
    """Check if the database is connected."""
    try:
        async with postgres_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

# Close database connections
async def close_db():
    """
    Close database connections.
    Call this on application shutdown.
    """
    await postgres_engine.dispose()