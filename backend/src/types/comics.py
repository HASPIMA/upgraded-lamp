from pydantic import BaseModel


class CreateFavoriteBody(BaseModel):
    comic_id: int
