import httpx
from fastapi import APIRouter, Response, status
from src.types.dependencies import AuthenticationDependant

from .utils import MARVEL_COMICS_URL, generate_params

router = APIRouter()


@router.get("/")
async def get_comics(
    _: AuthenticationDependant,
    response: Response,
):

    data = None
    errors = []

    try:
        async with httpx.AsyncClient() as client:
            params = generate_params()

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
