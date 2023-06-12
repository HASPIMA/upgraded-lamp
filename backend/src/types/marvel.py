from typing import TypedDict
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
    description: str
    image: str
