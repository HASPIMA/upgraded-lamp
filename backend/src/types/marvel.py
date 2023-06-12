from typing import Optional, TypedDict

from pydantic import BaseModel

MarvelParameters = TypedDict(
    "MarvelParameters",
    {
        'apikey': str,
        'ts': float,
        'hash': str,
        'offset': int,
    },
    total=True,
)


class Comic(BaseModel):
    id: int
    title: str
    description: Optional[str]
    image: str


class PaginatedComics(BaseModel):
    offset: int
    limit: int
    total: int
    count: int
    results: list[Comic]
