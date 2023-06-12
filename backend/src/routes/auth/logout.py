from typing import cast

from fastapi import APIRouter, Response, status
from prisma import Json, get_client
from prisma.errors import PrismaError
from prisma.models import usuarios
from src.types.dependencies import AuthenticationDependant

router = APIRouter(prefix="/logout")


@router.post("/")
async def logout(auth: AuthenticationDependant, response: Response):
    data = None
    errors = []
    status_code: int = status.HTTP_200_OK

    decoded_token, token = auth

    user = cast(usuarios, decoded_token['user'])

    try:
        # invalidate the token
        result = await get_client().tokens.create(
            data={
                'id_usuario': user.id,
                'token': Json(token),
                'invalidado': True,
            }
        )

        data = result
    except PrismaError as e:
        errors.append(e)

        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        print(type(e), e)

    except Exception as e:
        errors.append({
            'message': 'Internal server error.',
        })

        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        print(type(e), e)

    finally:
        response.status_code = status_code

        return {
            "data": data,
            "errors": errors,
        }
