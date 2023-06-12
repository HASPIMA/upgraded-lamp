from typing import Annotated, Optional

import httpx
from fastapi import APIRouter, Query, Response, status
from src.types.dependencies import AuthenticationDependant
from src.types.marvel import Comic
from src.types.responses import ComicResponse

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
):

    data = None
    errors = []

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

        results = [
            {
                "id": comic["id"],
                "title": comic["title"],
                "image": f"{comic['thumbnail']['path']}.{comic['thumbnail']['extension']}"
            }
            for comic in comics["data"]["results"]
        ]

        data = {
            'offset': comics['data']['offset'],
            'limit': comics['data']['limit'],
            'total': comics['data']['total'],
            'count': comics['data']['count'],
            'results': results
        }

    except Exception as e:
        errors.append(str(e))
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    finally:
        return {
            'data': data,
            'errors': errors
        }


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
        comic = comic['data']['results'][0]

        response_endpoint.data = Comic(
            id=comic['id'],
            title=comic['title'],
            description=comic['description'],
            image=f"{comic['thumbnail']['path']}.{comic['thumbnail']['extension']}"
        )

    except Exception as e:
        response_endpoint.errors.append(str(e))

        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    finally:
        return response_endpoint
