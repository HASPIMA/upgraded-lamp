import hashlib
from os import urandom


def hash_password(password: str):
    salt = urandom(32)
    hashed_password = hashlib.scrypt(
        password.encode('utf-8'),
        salt=salt,
        n=2 ** 14,
        r=8,
        p=1,
    )

    return hashed_password, salt
