from fastapi import APIRouter

from .root import router as root_router
from .favorites import router as favorites_router

router = APIRouter(prefix="/comics", tags=["comics"])

router.include_router(root_router)
router.include_router(favorites_router)
