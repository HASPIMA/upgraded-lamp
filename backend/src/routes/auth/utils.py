import hashlib
from base64 import b64decode, b64encode
from os import urandom, getenv
from typing import Optional

import jwt
from datetime import datetime
from prisma.models import usuarios


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


def generate_jwt(user: usuarios) -> str:
    """
    Generates a JWT for a user.

    Parameters
    ----------
    user : prisma.models.usuarios
        The user to generate the token for.

    Returns
    -------
    str
        The generated JWT token.
    """
    now = datetime.utcnow()

    _user = user.dict()
    _user.pop('contrasena')
    _user.pop('salt')

    return jwt.encode(
        {
            # User data without the password and salt
            'user': _user,

            # Subject is the user id
            'sub': user.id,

            # Issued at now
            'iat': now.timestamp(),

            # Expires in 1 minute by default if not specified
            'exp': now.timestamp() + int(getenv('JWT_EXPIRATION_TIME', 60)),
        },
        key='secret',
        algorithm='HS256',
    )
