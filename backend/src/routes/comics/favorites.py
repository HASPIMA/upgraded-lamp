import asyncio
from typing import Optional, cast

import httpx
from fastapi import APIRouter, Response, status
from prisma import get_client
from prisma.models import usuarios
from src.types.comics import CreateFavoriteBody
from src.types.dependencies import AuthenticationDependant
from src.types.marvel import Comic, MarvelParameters, PaginatedComics
from src.types.responses import ComicResponse, PaginatedComicsResponse

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
) -> PaginatedComicsResponse:
    result = PaginatedComicsResponse()

    user: usuarios = cast(usuarios, auth[0]['user'])

    try:
        favorites_ids = await get_client().favoritos.find_many(
            where={
                'id_usuario': user.id,
            },
        )

        # Define a coroutine to fetch the comic by ID
        async def fetch_comic(
            client: httpx.AsyncClient,
            params: MarvelParameters,
            comic_id: int,
        ) -> Optional[Comic]:
            '''
            Try to fetch a comic from the Marvel API by ID and convert it to
            a Comic object if successful or return None if not found or an
            error occurred.

            Parameters
            ----------
            client : httpx.AsyncClient
                The HTTP client to use

            params : MarvelParameters
                The parameters to use in the request

            comic_id : int
                The ID of the comic to fetch

            Returns
            -------
            Comic
                The comic fetched from the Marvel API

            None
                If the comic was not found or an error occurred
            '''
            response_marvel = await marvel_get_comic_by_id(
                client=client,
                params=params,
                id=comic_id,
            )

            if response_marvel.is_error:
                result.errors.append(str(response_marvel))
                return None

            comic = response_marvel.json()
            return convert_comics(comic)[0]

        # Create a list of coroutines to fetch the comics
        coroutines = []
        async with httpx.AsyncClient() as client:
            for favorite in favorites_ids:
                params = generate_params()
                coroutine = fetch_comic(client, params, favorite.id_comic)
                coroutines.append(coroutine)

            # Use asyncio.gather to run all coroutines concurrently
            comics = await asyncio.gather(*coroutines)

        # Remove None values and paginate the results
        comics = [comic for comic in comics if comic is not None]
        total_comics = len(comics)
        offset = 0
        limit = total_comics
        count = total_comics

        # TODO: Paginate the results
        result.data = PaginatedComics(
            results=comics,
            total=total_comics,
            offset=offset,
            limit=limit,
            count=count,
        )

    except httpx.HTTPStatusError as http_error:
        response.status_code = http_error.response.status_code
        result.errors.append(str(http_error))

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        result.errors.append(str(e))
    finally:
        return result
