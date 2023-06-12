from fastapi import APIRouter

from .root import router as root_router

router = APIRouter(prefix="/comics", tags=["comics"])

router.include_router(root_router)
