from redis.asyncio import Redis

from app.core.config import settings

redis_client: Redis | None = None


async def init_redis() -> Redis:
    global redis_client

    if redis_client is None:
        redis_client = Redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
        )

    return redis_client


async def get_redis() -> Redis:
    if redis_client is None:
        return await init_redis()

    return redis_client


async def close_redis() -> None:
    global redis_client

    if redis_client is not None:
        await redis_client.close()
        redis_client = None