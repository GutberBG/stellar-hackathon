"""Async SQLAlchemy database configuration and session management."""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()


async def init_db() -> None:
    """Creates database tables and applies lightweight SQLite column migrations."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        if "sqlite" in settings.DATABASE_URL:
            await _migrate_sqlite_producers(conn)


async def _migrate_sqlite_producers(conn) -> None:
    """Adds new producer columns to pre-existing SQLite databases."""
    result = await conn.exec_driver_sql("PRAGMA table_info(producers)")
    existing = {row[1] for row in result.fetchall()}
    migrations = {
        "hectares": "ALTER TABLE producers ADD COLUMN hectares FLOAT NOT NULL DEFAULT 2.0",
        "tree_age_years": "ALTER TABLE producers ADD COLUMN tree_age_years INTEGER NOT NULL DEFAULT 8",
        "altitude_m": "ALTER TABLE producers ADD COLUMN altitude_m FLOAT NOT NULL DEFAULT 500.0",
    }
    for column, ddl in migrations.items():
        if column not in existing:
            await conn.exec_driver_sql(ddl)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency for yielding database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
