from fastapi import APIRouter, Response
from prisma.client import get_client
from prisma.errors import PrismaError
from src.auth.utils import generate_jwt, hash_password
from src.types.user import SignupUser

router = APIRouter(prefix="/signup")


@router.post("/")
async def create_user(body: SignupUser, response: Response):
    data = None
    errors = []

    try:
        # hash the password
        hashed_password, salt = hash_password(body.contrasena)

        # create the user
        user = await get_client().usuarios.create(
            data={
                'nombre': body.nombre,
                'identificacion': body.identificacion,
                'correo_electronico': body.correo_electronico,
                'contrasena': hashed_password,
                'salt': salt,
            }
        )

        # remove the hashed password and salt from the response
        user.contrasena = ''
        user.salt = ''

        # generate the JWT and expiration time
        token, expires = generate_jwt(user)

        data = {
            'token': token,
            'expires': expires,
            'user': user,
        }
    except PrismaError as e:
        errors.append(e)

        response.status_code = 500

    finally:
        return {
            "data": data,
            "errors": errors,
        }
