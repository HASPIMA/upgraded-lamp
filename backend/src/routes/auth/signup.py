from fastapi import APIRouter, Response
from src.types.user import SignupUser

router = APIRouter(prefix="/signup")


@router.post("/")
async def create_user(body: SignupUser, response: Response):
    data = None
    errors = []

    return {
        "data": data,
        "errors": errors,
    }
