from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import configure_logging
from app.core.qdrant import close_qdrant, init_qdrant
from app.core.redis import close_redis, init_redis
from app.middleware.logging import LoggingMiddleware

from app.api.v1 import api_router

configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_redis()
    await init_qdrant()

    yield

    await close_redis()
    await close_qdrant()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    lifespan=lifespan,
)

app.add_middleware(LoggingMiddleware)


@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }

app.include_router(
    api_router,
    prefix=settings.API_V1_PREFIX,
)