
from typing import TypedDict

from prisma.models import usuarios

UserTokenPayload = TypedDict(
    "UserTokenPayload",
    {
        'user': usuarios,  # User
        'sub': int,  # Subject
        'iat': float,  # Issued at
        'nbf': float,  # Not before
        'exp': float,  # Expiration time
    },
    total=True,
)
