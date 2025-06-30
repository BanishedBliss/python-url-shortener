from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncEngine
from sqlalchemy.orm import declarative_base
from contextlib import asynccontextmanager

Base = declarative_base()

async_engine: AsyncEngine|None = None
AsyncSessionLocal: async_sessionmaker[AsyncSession]|None = None

# Инициализация БД: асинхронный движок и сессия
def init_db(database_url: str):
    global async_engine, AsyncSessionLocal
    async_engine = create_async_engine(database_url, echo=True)
    AsyncSessionLocal = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False
    )

@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def shutdown_db():
    await async_engine.dispose()