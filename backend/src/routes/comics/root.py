from typing import Annotated, Optional

import httpx
from fastapi import APIRouter, Query, Response, status
from src.types.dependencies import AuthenticationDependant

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
