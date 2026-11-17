from fastapi import APIRouter

from app.api.v1.projects import router as project_router
from app.api.v1.router import router as system_router

api_router = APIRouter()

api_router.include_router(project_router)
api_router.include_router(system_router)
