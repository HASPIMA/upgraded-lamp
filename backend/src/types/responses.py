from typing import Optional

from pydantic import BaseModel

from .marvel import Comic


class ComicResponse(BaseModel):
    data: Optional[Comic] = None
    errors: list = []
