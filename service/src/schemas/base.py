from datetime import datetime
from enum import Enum
from typing import Dict, Type
from uuid import UUID

from pydantic import BaseModel


class BaseData(BaseModel):
    user_id: UUID | str
    timestamp: datetime | str


class Click(BaseData):
    pass


class QualityChange(BaseData):
    pass


class CustomEvent(BaseData):
    pass


class Page(BaseData):
    pass


class Film(BaseData):
    pass


class KafkaTopic(Enum):
    CLICK = "click"
    CUSTOM_EVENT = "custom_event"
    FILM = "film"
    PAGE = "page"
    QUALITY_CHANGE = "quality_change"


# Отображение моделей на топики Kafka и таблицы ClickHouse
model_topic_map: Dict[str, Type[BaseData]] = {
    KafkaTopic.CLICK: Click,
    KafkaTopic.QUALITY_CHANGE: QualityChange,
    KafkaTopic.CUSTOM_EVENT: CustomEvent,
    KafkaTopic.PAGE: Page,
    KafkaTopic.FILM: Film,
}


# Создание SQL запросов для создания таблиц
def create_table_sql(topic: str) -> str:
    return f"CREATE TABLE IF NOT EXISTS {topic} (user_id String, timestamp DateTime) ENGINE = MergeTree() ORDER BY timestamp;"


# Создание SQL запросов для вставки данных
def insert_into_table_sql(topic: str, record: Dict) -> str:
    # Простой пример запроса для вставки данных
    fields = ", ".join(record.keys())
    values = ", ".join(
        f"'{value}'" if isinstance(value, str) else str(value)
        for value in record.values()
    )
    return f"INSERT INTO {topic} ({fields}) VALUES ({values});"
