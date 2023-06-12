from typing import Annotated, Optional

import httpx
from fastapi import APIRouter, Query, Response, status
from src.routes.comics.utils import convert_comics, to_paginated_comics
from src.types.dependencies import AuthenticationDependant
from src.types.responses import ComicResponse, PaginatedComicsResponse

from .utils import MARVEL_COMICS_URL, generate_params

router = APIRouter()


@router.get("/")
async def get_comics(
    _: AuthenticationDependant,
    response: Response,
    offset: Annotated[
        Optional[int],
        Query(
            title='Offset',
            description='The requested offset (number of skipped results) of the call.',
            ge=0,
        ),
    ] = None,
) -> PaginatedComicsResponse:

    response_endpoint = PaginatedComicsResponse()

    try:
        async with httpx.AsyncClient() as client:
            params = generate_params()

            if offset is not None:
                params['offset'] = offset

            response_marvel = await client.get(
                MARVEL_COMICS_URL,
                params=params,  # type: ignore
            )

        comics = response_marvel.json()

        results = convert_comics(comics)

        response_endpoint.data = to_paginated_comics(comics, results)

    except Exception as e:
        response_endpoint.errors.append(str(e))
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    finally:
        return response_endpoint


@router.get("/{comic_id}")
async def get_comic_by_id(
    _: AuthenticationDependant,
    response: Response,
    comic_id: int,
) -> ComicResponse:
    response_endpoint = ComicResponse()

    try:
        async with httpx.AsyncClient() as client:
            params = generate_params()

            response_marvel = await client.get(
                f"{MARVEL_COMICS_URL}/{comic_id}",
                params=params,  # type: ignore
            )

        comic = response_marvel.json()

        response_endpoint.data = convert_comics(comic)[0]

    except Exception as e:
        response_endpoint.errors.append(str(e))

        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    finally:
        return response_endpoint
