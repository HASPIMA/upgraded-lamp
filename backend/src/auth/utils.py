import hashlib
from base64 import b64decode, b64encode
from os import urandom, getenv
from typing import Optional

import jwt
from datetime import datetime, timezone
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


def generate_jwt(user: usuarios) -> tuple[str, datetime]:
    """
    Generates a JWT for a user.

    Parameters
    ----------
    user : prisma.models.usuarios
        The user to generate the token for.

    Returns
    -------
    tuple[str, datetime]
        A tuple containing the JWT and the expiration time.
    """
    now = datetime.now(tz=timezone.utc)

    _user = user.dict()
    _user.pop('contrasena')
    _user.pop('salt')

    expires = now.timestamp() + int(getenv('JWT_EXPIRATION_TIME', 60))

    token = jwt.encode(
        {
            # User data without the password and salt
            'user': _user,

            # Subject is the user id
            'sub': user.id,

            # Issued at now
            'iat': now.timestamp(),

            # Expires in 1 minute by default if not specified
            'exp': expires,
        },
        key='secret',
        algorithm='HS256',
    )

    return (
        token,
        # Return the expiration time as a datetime object
        # timezone is set to UTC
        datetime.fromtimestamp(expires, tz=timezone.utc),
    )
