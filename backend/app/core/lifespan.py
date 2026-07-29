from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config.settings import get_settings
from app.core.logging.setup import setup_logging
from app.database.session import close_database, init_database
from app.memory.qdrant import close_qdrant, init_qdrant
from app.memory.redis import close_redis, init_redis


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    setup_logging(settings.log_level)

    await init_database(settings.database_url)
    await init_redis(settings.redis_url)
    await init_qdrant(url=settings.qdrant_url, api_key=settings.qdrant_api_key)
    try:
        yield
    finally:
        await close_qdrant()
        await close_redis()
        await close_database()
