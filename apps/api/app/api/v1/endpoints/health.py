from fastapi import APIRouter, Depends

from app.dependencies import get_settings_dependency
from core.config.settings import Settings
from shared.schemas.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def healthcheck(settings: Settings = Depends(get_settings_dependency)) -> HealthResponse:
    return HealthResponse(status="ok", service=settings.app_name, api_version="v1")
