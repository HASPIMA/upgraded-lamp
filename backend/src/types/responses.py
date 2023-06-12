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


class FavoritosResponse(BaseModel):
    data: Optional[favoritos] = None
    errors: list = []


class FavoritosManyResponse(BaseModel):
    data: Optional[list[favoritos]] = None
    errors: list = []
