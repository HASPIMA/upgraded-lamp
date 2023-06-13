from typing import Optional

from prisma.models import favoritos
from pydantic import BaseModel

from .marvel import Comic, PaginatedComics


class PaginatedComicsResponse(BaseModel):
    data: Optional[PaginatedComics] = None
    errors: list = []


class ComicResponse(BaseModel):
    data: Optional[Comic] = None
    errors: list = []
