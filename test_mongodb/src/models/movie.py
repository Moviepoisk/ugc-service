from beanie import Document
from pydantic import Field


class MovieDocument(Document):
    title: str
    year: int
    genre: str
    likes: int = Field(default=0, description="Количество лайков")
    dislikes: int = Field(default=0, description="Количество дизлайков")
    ratings: list[float] = Field(default_factory=list, description="Список пользовательских рейтингов")

    @property
    def average_rating(self) -> float:
        """Средняя пользовательская оценка фильма"""
        if not self.ratings:
            return 0.0
        return sum(self.ratings) / len(self.ratings)

    class Settings:
        collection = "movies"
