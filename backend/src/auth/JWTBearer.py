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

        response = {
            'data': None,
            'errors': [],
        }

        def add_error(message: str, details: Optional[dict] = None):
            response['errors'].append(
                {
                    'message': message,
                    'details': details,
                }
            )

        if credentials:
            if not credentials.scheme == "Bearer":
                add_error('Invalid authentication scheme.')

                raise HTTPException(
                    status_code=401,
                    detail=response
                )

            try:
                decoded_token = decode_and_verify_jwt(credentials.credentials)
            except jwt.exceptions.InvalidTokenError as e:
                add_error('Invalid token or expired token.')

                raise HTTPException(
                    status_code=400,
                    detail=response,
                ) from e

            if not isinstance(decoded_token, dict):
                add_error('Invalid token or expired token.')

                raise HTTPException(
                    status_code=401,
                    detail=response,
                )

            uid: Optional[int] = decoded_token.get('sub')
            user_token: Optional[dict] = decoded_token.get('user')

            # TODO: Check if the user exists in the database
            # TODO: Check subject and user id match

            # Prepare the response
            add_error('Invalid token.')

            # Check if the token's subject and user id are valid
            if uid is None or \
                    user_token is None or \
                    not isinstance(uid, int) or \
                    not isinstance(user_token, dict):
                raise HTTPException(
                    status_code=400,
                    detail=response,
                )

            return decoded_token

        add_error('Invalid authorization code.')

        raise HTTPException(
            status_code=401,
            detail=response,
        )
