from datetime import datetime, timezone
from hashlib import md5
from os import getenv
from src.types.marvel import MarvelParameters

import httpx
from src.types.marvel import Comic, PaginatedComics

from src.types.marvel import MarvelParameters

MARVEL_PRIVATE_KEY = getenv('MARVEL_PRIVATE_KEY', '')
MARVEL_PUBLIC_KEY = getenv('MARVEL_PUBLIC_KEY', '')

MARVEL_COMICS_URL = 'https://gateway.marvel.com/v1/public/comics'


def generate_hash() -> tuple[str, float]:
    """
    Generates a hash and a timestamp to be used in the Marvel API requests.

    Returns
    -------
    tuple[str, float]
        A tuple containing the hash and the timestamp.
    """
    timestamp = datetime.now(tz=timezone.utc).timestamp()
    data = f'{timestamp}{MARVEL_PRIVATE_KEY}{MARVEL_PUBLIC_KEY}'.encode()

    hash = md5(data).hexdigest()
    return hash, timestamp


def generate_params() -> MarvelParameters:
    """
    Generates the params to be used in the Marvel API requests.

    Returns
    -------
    src.types.marvel.MarvelParameters
        A dictionary containing the params.
    """
    hash, timestamp = generate_hash()

    return {
        'apikey': MARVEL_PUBLIC_KEY,
        'ts': timestamp,
        'hash': hash,
        'offset': 0,
    }


def convert_comics(comics: dict) -> list[Comic]:
    '''
    Converts the comics from the Marvel API to the Comic model.

    Parameters
    ----------
    comics : dict
        The comics from the Marvel API.

    Returns
    -------
    list[Comic]
        A list of Comic models.
    '''
    return [
        Comic(
            id=comic['id'],
            title=comic['title'],
            description=comic['description'],
            image=f"{comic['thumbnail']['path']}.{comic['thumbnail']['extension']}"
        )
        for comic in comics["data"]["results"]
    ]


def to_paginated_comics(comics: dict, results: list[Comic]) -> PaginatedComics:
    '''
    Converts the comics from the Marvel API to the PaginatedComics model.

    Parameters
    ----------
    comics : dict
        The comics from the Marvel API.

    results : list[Comic]
        The comics converted to the Comic model.

    Returns
    -------
    PaginatedComics
        A PaginatedComics model.
    '''
    return PaginatedComics(
        offset=comics['data']['offset'],
        limit=comics['data']['limit'],
        total=comics['data']['total'],
        count=comics['data']['count'],
        results=results,
    )


async def marvel_get_comic_by_id(
    *,
    client: httpx.AsyncClient,
    params: MarvelParameters,
    id: int,
) -> httpx.Response:
    '''
    Gets a comic from the Marvel API by its id.

    Parameters
    ----------
    client : httpx.AsyncClient
        The httpx client.

    params : src.types.marvel.MarvelParameters
        The params to be used in the Marvel API request.

    id : int
        The id of the comic.

    Returns
    -------
    httpx.Response
        The response from the Marvel API.
    '''
    response_marvel = await client.get(
        f"{MARVEL_COMICS_URL}/{id}",
        params=params,  # type: ignore
    )

    return response_marvel
