from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as v1_router
from app.core.config.settings import get_settings
from app.core.lifespan import lifespan
from app.middleware.error_handler import ErrorHandlingMiddleware

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="TwinPilot backend API foundation",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ErrorHandlingMiddleware)

app.include_router(v1_router, prefix=settings.api_v1_prefix)
