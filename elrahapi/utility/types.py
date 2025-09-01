from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TypeAlias

ElrahSession : TypeAlias = Session|AsyncSession


from pydantic import BaseModel
class CountModel(BaseModel):
    total_count: int
    daily_total_count: int
    seven_previous_day_total_count: int
    monthly_total_count: int
