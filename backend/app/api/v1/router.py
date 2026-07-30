from fastapi import APIRouter

from app.api.v1.endpoints.health import router as health_router

router = APIRouter()
router.include_router(health_router)  # to check system status and diagnostic endpoints

"""In FastAPI, an APIRouter acts as a "mini FastAPI" application. It is a tool used to organize your 
code by splitting a large application into multiple smaller, manageable files, rather than 
stuffing every single API endpoint into one massive main.py file."""