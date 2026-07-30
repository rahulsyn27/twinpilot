"""Vector database"""
from qdrant_client import AsyncQdrantClient

from app.core.config import settings

qdrant_client: AsyncQdrantClient | None = None


async def init_qdrant() -> AsyncQdrantClient:
    global qdrant_client

    if qdrant_client is None:
        qdrant_client = AsyncQdrantClient(
            url=settings.QDRANT_URL,
        )

    return qdrant_client


async def get_qdrant() -> AsyncQdrantClient:
    if qdrant_client is None:
        return await init_qdrant()

    return qdrant_client


async def close_qdrant() -> None:
    global qdrant_client

    if qdrant_client is not None:
        await qdrant_client.close()
        qdrant_client = None