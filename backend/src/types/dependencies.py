from typing import Annotated

from fastapi import Depends
from src.auth.JWTBearer import JWTBearer
from src.types.token import UserTokenPayload

AuthenticationToken = Annotated[UserTokenPayload, Depends(JWTBearer())]
