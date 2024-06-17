from datetime import datetime
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
