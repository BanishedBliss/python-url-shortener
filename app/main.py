from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.config import settings
from .database import init_db, create_tables, shutdown_db
from .endpoints import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализация БД
    init_db(settings.DATABASE_URL)
    await create_tables()
    yield
    # Очистка
    await shutdown_db()

app = FastAPI(lifespan=lifespan)
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT
    )