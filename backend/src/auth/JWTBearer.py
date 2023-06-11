from typing import Optional

import jwt
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from prisma import get_client
from prisma.models import usuarios
from src.types.token import UserTokenPayload

from .utils import decode_and_verify_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> UserTokenPayload:
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
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=response
                )

            try:
                decoded_token = decode_and_verify_jwt(credentials.credentials)
            except jwt.exceptions.InvalidTokenError as e:
                add_error('Invalid token or expired token.')

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=response,
                ) from e

            if not isinstance(decoded_token, dict):
                add_error('Invalid token or expired token.')

                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=response,
                )

            uid: Optional[int] = decoded_token.get('sub')
            user_token: Optional[usuarios] = decoded_token.get('user')

            # Prepare the response
            add_error('Invalid token.')

            # Check if the token's subject and user id are valid
            if uid is None or \
                    user_token is None or \
                    not isinstance(uid, int) or \
                    not isinstance(user_token, dict):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=response,
                )

            # Check subject and user id match
            if uid != user_token.get('id'):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=response,
                )

            # Check if the user exists in the database
            user: Optional[usuarios] = await get_client().usuarios.find_unique(
                where={
                    'id': uid,
                }
            )

            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=response,
                )

            decoded_token['user'] = user

            return decoded_token

        add_error('Invalid authorization code.')

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=response,
        )
