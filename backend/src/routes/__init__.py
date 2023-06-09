from .auth import router as auth_router
from fastapi import APIRouter

routes = APIRouter()


routes.include_router(auth_router)

__all__ = ["routes"]
