from typing import Any, TypedDict, Union

from prisma.models import usuarios

UserPayload = Union[usuarios, dict[str, Any]]

UserTokenPayload = TypedDict(
    "UserTokenPayload",
    {
        'user': UserPayload,  # User
        'sub': int,  # Subject
        'iat': float,  # Issued at
        'nbf': float,  # Not before
        'exp': float,  # Expiration time
    },
    total=True,
)
