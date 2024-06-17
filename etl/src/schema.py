import json
from uuid import UUID

from pydantic import BaseModel, ValidationError


class ClickData(BaseModel):
    user_id: UUID
    timestamp: str


SQL_CREATE_TABLE_CLICK = """
    CREATE TABLE IF NOT EXISTS click (
            user_id UUID,
            event_time DateTime,
        ) ENGINE = MergeTree()
        ORDER BY (event_time, user_id)
    """
SQL_INSERT_INTO_TABLE_CLICK = """
    INSERT INTO click (user_id, event_time) VALUES
    """


class QaChangeData(BaseModel):
    user_id: UUID
    timestamp: str


class PageData(BaseModel):
    user_id: UUID
    timestamp: str


class Finish(BaseModel):
    user_id: UUID
    timestamp: str


class Search(BaseModel):
    user_id: UUID
    timestamp: str


def append_data_from_message(buffer, message_value, model):
    try:
        data = model.parse_raw(message_value)
        buffer.append(data.dict().values())
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON: {e} - Содержимое: {message_value}")
    except ValidationError as e:
        print(f"Ошибка валидации данных: {e} - Содержимое: {message_value}")