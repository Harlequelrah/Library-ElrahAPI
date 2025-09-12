from pydantic import BaseModel

from datetime import datetime


class CountModel(BaseModel):
    total_count: int
    daily_total_count: int
    seven_previous_day_total_count: int
    monthly_total_count: int


class AdditionalSchemaFields:
    date_created: datetime
    date_updated: datetime
    date_deleted: datetime | None = None
    is_deleted: bool
