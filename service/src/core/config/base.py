from enum import StrEnum

from pydantic_settings import BaseSettings, SettingsConfigDict


class KafkaTopic(StrEnum):
    CLICK = "click"
    CUSTOM_EVENT = "custom_event"
    FILM = "film"
    PAGE = "page"
    QUALITY_CHANGE = "quality_change"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file_encoding="utf-8",
        env_file=".env",
    )

    debug: bool = True
    name: str = "ugc_service"
    host: str = "ugc_service"
    port: int = 5000
    workers: int = 4
    log_level: str = "info"

    kafka_bootstrap_servers: str
    kafka_num_partitions: int = 3
    kafka_replication_factor: int = 2
    kafka_acks: str = "all"


settings = Settings()
