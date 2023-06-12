from fastapi import APIRouter

from .signup import router as signup_router
from .login import router as login_router
from .logout import router as logout_router

router = APIRouter(prefix="/auth", tags=["auth"])

router.include_router(signup_router)
router.include_router(login_router)
router.include_router(logout_router)
