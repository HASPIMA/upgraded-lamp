from typing import cast

import httpx
from fastapi import APIRouter, Response, status
from prisma import get_client
from prisma.models import usuarios
from src.types.comics import CreateFavoriteBody
from src.types.dependencies import AuthenticationDependant
from src.types.responses import ComicResponse, FavoritosManyResponse

from .utils import convert_comics, generate_params, marvel_get_comic_by_id

router = APIRouter(prefix='/favorites', tags=['favorites'])


@router.post('/')
async def save_favorite(
    auth: AuthenticationDependant,
    response: Response,
    comic_body: CreateFavoriteBody,
) -> ComicResponse:
    response_endpoint = ComicResponse()

    user: usuarios = cast(usuarios, auth[0]['user'])

    try:
        favorite = await get_client().favoritos.create(
            data={
                'id_usuario': user.id,
                'id_comic': comic_body.comic_id,
            },
        )

        # Fetch the comic from the Marvel API and return it
        async with httpx.AsyncClient() as client:
            params = generate_params()

            response_marvel = await marvel_get_comic_by_id(
                client=client,
                params=params,
                id=favorite.id_comic,
            )

        response_marvel.raise_for_status()

        comic = response_marvel.json()

        response_endpoint.data = convert_comics(comic)[0]

    except httpx.HTTPStatusError as http_error:
        response.status_code = http_error.response.status_code
        response_endpoint.errors.append(str(http_error))

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
    except httpx.HTTPStatusError as http_error:
        response.status_code = http_error.response.status_code
        result.errors.append(str(http_error))

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        result.errors.append(str(e))
    finally:
        return result
