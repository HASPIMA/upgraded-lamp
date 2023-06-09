from fastapi import APIRouter

from .signup import router as signup_router

router = APIRouter(prefix="/auth", tags=["auth"])

router.include_router(signup_router)
