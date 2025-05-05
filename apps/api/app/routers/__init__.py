from .profile import router as profile_router
from .preferences import router as preferences_router
from .tasks       import router as tasks_router
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(profile_router)
api_router.include_router(preferences_router)
api_router.include_router(tasks_router)
