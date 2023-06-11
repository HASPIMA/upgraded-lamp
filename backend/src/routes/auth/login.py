from fastapi import APIRouter,  Response, status
from prisma.client import get_client
from prisma.errors import PrismaError
from src.types.user import LoginUser

from .utils import verify_password

router = APIRouter(prefix="/login")


@router.post("/")
async def login(body: LoginUser, response: Response):
    data = None
    errors = []
    status_code: int = status.HTTP_200_OK

    try:
        user = await get_client().usuarios.find_unique(
            where={
                'correo_electronico': body.correo_electronico,
            }
        )

        if user is None:
            status_code = status.HTTP_404_NOT_FOUND
            raise PrismaError('User not found.')

        if not verify_password(user, body.contrasena):
            status_code = status.HTTP_403_FORBIDDEN
            raise PrismaError('Incorrect password.')

    except PrismaError as e:
        errors.append(e)

        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    finally:
        response.status_code = status_code

        return {
            "data": data,
            "errors": errors,
        }
