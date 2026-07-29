from qdrant_client.async_qdrant_client import AsyncQdrantClient

_qdrant_client: AsyncQdrantClient | None = None


async def init_qdrant(url: str, api_key: str | None = None) -> None:
    global _qdrant_client
    _qdrant_client = AsyncQdrantClient(url=url, api_key=api_key)
    await _qdrant_client.get_collections()


async def close_qdrant() -> None:
    global _qdrant_client
    if _qdrant_client is not None:
        await _qdrant_client.close()
    _qdrant_client = None


def get_qdrant_client() -> AsyncQdrantClient:
    if _qdrant_client is None:
        raise RuntimeError("Qdrant client has not been initialized.")
    return _qdrant_client
