from datetime import datetime, timezone
from hashlib import md5
from os import getenv


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
