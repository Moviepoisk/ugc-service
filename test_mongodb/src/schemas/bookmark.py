from pydantic import BaseModel


class BookmarkSchema(BaseModel):
    url: str
    title: str
    description: str = None
