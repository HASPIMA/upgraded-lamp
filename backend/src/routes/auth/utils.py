import hashlib
from base64 import b64encode
from typing import Optional
from os import urandom


def hash_password(password: str, salt: Optional[bytes] = None) -> tuple[str, str]:
    """
    Hashes a password using the scrypt algorithm.

    Parameters
    ----------
    password : str
        The password to hash.
    salt : Optional[bytes], optional
        The salt to use. If not provided, a random salt will be generated.

    Returns
    -------
    tuple[str, str]
        A tuple containing the hashed password and the salt used.
    """

    if salt is None:
        salt = urandom(32)

    hashed_password = hashlib.scrypt(
        password.encode('utf-8'),
        salt=salt,
        n=2 ** 14,
        r=8,
        p=1,
    )

    return b64encode(hashed_password).decode('utf-8'), b64encode(salt).decode('utf-8')
