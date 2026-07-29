from typing import AsyncIterator

from qdrant_client.async_qdrant_client import AsyncQdrantClient
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config.settings import Settings, get_settings
from app.database.session import get_db_session
from app.memory.qdrant import get_qdrant_client
from app.memory.redis import get_redis_client


def get_settings_dependency() -> Settings:
    return get_settings()


async def get_db_session_dependency() -> AsyncIterator[AsyncSession]:
    async for session in get_db_session():
        yield session


def get_redis_dependency() -> Redis:
    return get_redis_client()


def get_qdrant_dependency() -> AsyncQdrantClient:
    return get_qdrant_client()
