from fastapi import APIRouter

from .signup import router as signup_router
from .login import router as login_router

router = APIRouter(prefix="/auth", tags=["auth"])

router.include_router(signup_router)
router.include_router(login_router)
