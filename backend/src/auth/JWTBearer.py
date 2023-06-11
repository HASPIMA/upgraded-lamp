from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

import jwt
from .utils import decode_and_verify_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        credentials: Optional[HTTPAuthorizationCredentials] = await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=401,
                    detail="Invalid authentication scheme."
                )

            try:
                decoded_token = decode_and_verify_jwt(credentials.credentials)
            except jwt.exceptions.InvalidTokenError as e:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid token or expired token.",
                ) from e

            if not decoded_token:
                raise HTTPException(
                    status_code=403,
                    detail="Invalid token or expired token."
                )

            return decoded_token

        raise HTTPException(
            status_code=401,
            detail="Invalid authorization code."
        )
