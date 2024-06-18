from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file_encoding="utf-8",
        env_file=".env",
    )

    debug: bool = True
    name: str = "etl_service"
    host: str = "etl_service"
    log_level: str = "info"

    kafka_host: str
    kafka_num_partitions: int = 3
    kafka_replication_factor: int = 2
    kafka_acks: str = "all"

    clickhouse_group: str = "clickhouse_group"
    clickhouse_connection_url: str = "clickhouse://default:@localhost/default"


settings = Settings()
