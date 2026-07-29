from redis.asyncio import Redis

_redis_client: Redis | None = None


async def init_redis(redis_url: str) -> None:
    global _redis_client
    _redis_client = Redis.from_url(redis_url, encoding="utf-8", decode_responses=True)
    await _redis_client.ping()


async def close_redis() -> None:
    global _redis_client
    if _redis_client is not None:
        await _redis_client.aclose()
    _redis_client = None


def get_redis_client() -> Redis:
    if _redis_client is None:
        raise RuntimeError("Redis client has not been initialized.")
    return _redis_client
