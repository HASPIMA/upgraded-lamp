from typing import TypedDict

MarvelParameters = TypedDict(
    "MarvelParameters",
    {
        'apikey': str,
        'ts': float,
        'hash': str,
    },
    total=True,
)
