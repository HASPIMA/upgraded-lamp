from typing import TypedDict

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
