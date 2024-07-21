from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for test_mongodb project."""

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file_encoding="utf-8",
    )

    host: str = "localhost"
    port: int = 27017
    movie_amount: int = 10_000
    user_amount: int = 1000

    def get_dsn(self):
        """Метод получения dsn для подключения к MongoDB."""
        return f"mongodb://{self.host}:{self.port}"


settings = Settings()
