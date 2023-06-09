from fastapi import APIRouter, Response
from prisma.client import get_client
from prisma.errors import PrismaError
from src.types.user import SignupUser

from .utils import hash_password

router = APIRouter(prefix="/signup")


@router.post("/")
async def create_user(body: SignupUser, response: Response):
    data = None
    errors = []

    try:
        # hash the password
        hashed_password, salt = hash_password(body.contrasena)

        # create the user
        data = await get_client().usuarios.create(
            data={
                'nombre': body.nombre,
                'identificacion': body.identificacion,
                'correo_electronico': body.correo_electronico,
                'contrasena': hashed_password,
                'salt': salt,
            }
        )

        # remove the hashed password and salt from the response
        data.contrasena = ''
        data.salt = ''
    except PrismaError as e:
        errors.append(e)

        response.status_code = 500

    finally:
        return {
            "data": data,
            "errors": errors,
        }
