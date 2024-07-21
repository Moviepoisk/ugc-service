from beanie import Document, PydanticObjectId
from pydantic import Field

from src.schemas import BookmarkSchema


class UserDocument(Document):
    user_id: str = Field(..., description="Unique identifier for the user")
    liked_movies: list[PydanticObjectId] = Field(default_factory=list, description="Список лайков пользователя")
    bookmarks: list[BookmarkSchema] = Field(default_factory=list, description="Список закладок")

    class Settings:
        collection = "users"
