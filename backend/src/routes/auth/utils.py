import hashlib
from base64 import b64encode, b64decode
from typing import Optional
from prisma.models import usuarios
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
        A tuple containing the hashed password and the salt used base64 encoded.
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


def verify_password(user: usuarios, password: str) -> bool:
    """
    Verifies a password against the one stored in the database.

    Parameters
    ----------
    user : prisma.models.usuarios
        The user to verify the password against.
    password : str
        The password to verify.

    Returns
    -------
    bool
        Whether the password is correct or not.
    """

    hashed_password, _ = hash_password(password, b64decode(user.salt))

    return user.contrasena == hashed_password
