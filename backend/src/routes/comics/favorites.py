from typing import cast

from fastapi import APIRouter, Response, status
from prisma import get_client
from prisma.models import usuarios
from src.types.comics import CreateFavoriteBody
from src.types.dependencies import AuthenticationDependant
from src.types.responses import FavoritosManyResponse, FavoritosResponse

router = APIRouter(prefix='/favorites', tags=['favorites'])


@router.post('/')
async def save_favorite(
    auth: AuthenticationDependant,
    response: Response,
    comic_body: CreateFavoriteBody,
) -> FavoritosResponse:
    response_endpoint = FavoritosResponse()

    user: usuarios = cast(usuarios, auth[0]['user'])

    try:
        favorite = await get_client().favoritos.create(
            data={
                'id_usuario': user.id,
                'id_comic': comic_body.comic_id,
            },
        )

        response_endpoint.data = favorite

        # TODO: fetch the comic from the Marvel API and return them
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response_endpoint.errors.append(str(e))
    finally:
        return response_endpoint


@router.get('/')
async def get_all_favorites(
    auth: AuthenticationDependant,
    response: Response,
) -> FavoritosManyResponse:
    result = FavoritosManyResponse()

    user: usuarios = cast(usuarios, auth[0]['user'])

    try:
        favorites = await get_client().favoritos.find_many(
            where={
                'id_usuario': user.id,
            },
        )

        result.data = favorites
        # TODO: fetch the comics from the Marvel API and return them
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        result.errors.append(str(e))
    finally:
        return result
