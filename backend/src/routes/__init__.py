from fastapi import APIRouter

from .auth import router as auth_router
from .comics import router as comics_router

routes = APIRouter()


routes.include_router(auth_router)
routes.include_router(comics_router)

__all__ = ["routes"]
