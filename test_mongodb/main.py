import asyncio

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from src.models import MovieDocument, UserDocument
from src.services.gen_data import MovieFaker, UserFaker, Faker
from src.services.utils import speedtest
from src.config import settings


async def init():
    print("Initializing Mongodb client")
    client = AsyncIOMotorClient(settings.get_dsn())
    await init_beanie(database=client.db_name, document_models=[UserDocument, MovieDocument])
    print("Mongodb client is ready")


async def before_script(fakers: list[Faker]) -> None:
    print("Starting to delete all documents")
    for faker in fakers:
        await faker.delete_all()
    print("All documents are deleted")


@speedtest
async def write_data(
    movie_faker: MovieFaker, user_faker: UserFaker, movie_amount: int = 1_000, user_amount: int = 1_000
) -> None:
    movies = await movie_faker.gen_data(amount=movie_amount)
    print(f"Movies generated: {movie_amount} items")
    await movie_faker.insert_documents(documents=movies)
    print("Movies inserted to MongoDB")

    users = await user_faker.gen_data(amount=user_amount, movies=movies[:10])
    print(f"Users generated: {user_amount} items")
    await user_faker.insert_documents(documents=users)
    print("Users inserted to MongoDB")

    retrieved_movie = await movie_faker.get_one(movies=movies)

    print(f"Average rating for {retrieved_movie.title}: {retrieved_movie.average_rating}")
    print(f"Likes: {retrieved_movie.likes}, Dislikes: {retrieved_movie.dislikes}")

    retrieved_user = await user_faker.get_one(users=users)
    print(retrieved_user)


@speedtest
async def read_data(movie_faker: MovieFaker, user_faker: UserFaker):
    movies = await movie_faker.read_all()
    print(f"Movies fetched: {len(movies)} items")

    users = await user_faker.read_all()
    print(f"Users fetched: {len(users)} items")


async def main(movie_amount: int = 10_000, user_amount: int = 1_000):
    movie_faker = MovieFaker()
    user_faker = UserFaker()

    await init()
    await before_script(fakers=[movie_faker, user_faker])
    await write_data(movie_faker=movie_faker, user_faker=user_faker, movie_amount=movie_amount, user_amount=user_amount)
    await read_data(movie_faker=movie_faker, user_faker=user_faker)


if __name__ == "__main__":
    asyncio.run(main(movie_amount=settings.movie_amount, user_amount=settings.user_amount))
