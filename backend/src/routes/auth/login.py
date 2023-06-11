from fastapi import APIRouter, Response, status
from prisma.client import get_client
from prisma.errors import PrismaError
from src.auth.utils import generate_jwt, verify_password
from src.types.user import LoginUser

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

        # Remove the password and salt from the user data
        _user = user
        _user.contrasena = ''
        _user.salt = ''

        # generate the JWT and expiration time
        token, expires = generate_jwt(_user)

        data = {
            'token': token,
            'expires': expires,
            'user': _user,
        }

    except PrismaError as e:
        errors.append(e)

        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    finally:
        response.status_code = status_code

        return {
            "data": data,
            "errors": errors,
        }
