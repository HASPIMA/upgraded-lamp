from typing import Optional

import jwt
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.types.token import UserPayload, UserTokenPayload
from prisma import Json, get_client
from prisma.errors import PrismaError
from prisma.models import tokens, usuarios

from .utils import decode_and_verify_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> tuple[UserTokenPayload, str]:
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

            credential_token = credentials.credentials

            try:
                decoded_token = decode_and_verify_jwt(credential_token)
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
            user_token: Optional[UserPayload] = decoded_token.get('user')

            # Check if the token's subject and user id are valid
            if uid is None or \
                    user_token is None or \
                    not isinstance(uid, int) or \
                    not isinstance(user_token, dict):
                add_error('Invalid token.')

                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=response,
                )

            # Check subject and user id match
            if uid != user_token.get('id'):
                add_error('Invalid token.')

                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=response,
                )

            # Check token is not invalidated
            try:
                token_db: Optional[tokens] = await get_client().tokens.find_first(
                    where={
                        'id_usuario': uid,
                        'token': {
                            'equals': Json(credential_token),
                        },
                        'invalidado': True,
                    }
                )

                if token_db is not None and token_db.invalidado:
                    add_error('Invalid token.')

                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=response,
                    )
            except PrismaError as e:
                add_error('Internal server error.')

                print(f'Error getting token ({credential_token}):')
                print(type(e), e)

                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=response,
                ) from e

            # Check if the user exists in the database
            try:
                user: Optional[usuarios] = await get_client().usuarios.find_unique(
                    where={
                        'id': uid,
                    },
                    include={
                        'favoritos': True,
                    },
                )

            except Exception as e:
                add_error('Internal server error.')

                print(f'Error getting user ({uid}):')
                print(type(e), e)

                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=response,
                ) from e

            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=response,
                )

            decoded_token['user'] = user

            return decoded_token, credential_token

        add_error('Invalid authorization code.')

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=response,
        )
