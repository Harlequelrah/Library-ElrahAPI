from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


class MetaLogModel:
    id: Mapped[int] = mapped_column(primary_key=True)
    status_code: Mapped[int] = mapped_column(index=True)
    method: Mapped[str] = mapped_column(String(30))
    url: Mapped[str]
    error_message: Mapped[str] = mapped_column(Text)
    date_created: Mapped[datetime] = mapped_column(default=func.now())
    remote_address: Mapped[str]
    process_time: Mapped[float] = mapped_column(Numeric(precision=10, scale=6))


class MetaLogReadModel(BaseModel):
    id: int
    status_code: int
    method: str
    url: str
    error_message: str | None = None
    date_created: datetime
    process_time: float
    remote_address: str
