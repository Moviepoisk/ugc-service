import random
import string

from beanie import Document
from pydantic import BaseModel

from src.schemas import BookmarkSchema
from src.models import MovieDocument, UserDocument


class Faker:
    beanie_document = None

    @classmethod
    def _random_string(cls, length=10):
        letters = string.ascii_letters
        return "".join(random.choice(letters) for _ in range(length))

    async def gen_data(self, *args, **kwargs) -> type[BaseModel]:
        pass

    async def delete_all(self) -> None:
        await self.beanie_document.delete_all()

    async def read_all(self) -> list[Document] | None:
        return await self.beanie_document.find().to_list()

    async def insert_documents(self, documents: list[type[Document]] | list[Document]) -> None:
        await self.beanie_document.insert_many(documents)


class MovieFaker(Faker):
    beanie_document = MovieDocument
    genres = ["Action", "Comedy", "Drama", "Horror", "Sci-Fi"]

    async def gen_data(self, amount: int = 1_000) -> list[Document]:
        return [
            self.beanie_document(
                title=self._random_string(length=10),
                year=random.randint(1960, 2024),
                genre=random.choice(self.genres),
                likes=random.randint(0, 100),
                dislikes=random.randint(0, 100),
                ratings=[random.uniform(1, 10) for _ in range(random.randint(1, 100))],
            )
            for _ in range(amount)
        ]

    async def get_one(self, movies: list[MovieDocument] | list[Document] = None) -> Document:
        return await self.beanie_document.find_one(self.beanie_document.title == movies[0].title)


class UserFaker(Faker):
    beanie_document = UserDocument

    async def __gen_bookmarks(self) -> list[BaseModel]:
        return [
            BookmarkSchema(
                url=f"https://{self._random_string(length=10)}.com",
                title=self._random_string(10),
                description=self._random_string(20),
            )
            for _ in range(random.randint(1, 20))
        ]

    async def gen_data(
        self, amount: int = 1_000, movies: list[MovieDocument] | list[Document] = None
    ) -> list[Document]:
        liked_movies = random.sample([movie.id for movie in movies], k=random.randint(1, len(movies)))
        return [
            self.beanie_document(
                user_id=self._random_string(length=10),
                liked_movies=liked_movies,
                bookmarks=await self.__gen_bookmarks(),
            )
            for _ in range(amount)
        ]

    async def get_one(self, users: list[UserDocument] | list[Document] = None) -> Document:
        return await self.beanie_document.find_one(self.beanie_document.user_id == users[0].user_id)
