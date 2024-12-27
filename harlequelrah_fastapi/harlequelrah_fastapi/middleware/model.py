from typing import Optional
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Numeric
)
from pydantic import BaseModel, Field
from datetime import datetime

from sqlalchemy.sql import func



class LoggerMiddlewareModel:
    id = Column(Integer, primary_key=True, index=True)
    status_code = Column(Integer, index=True)
    method = Column(String(30), nullable=False)
    url = Column(String(255), nullable=False)
    error_message=Column(String(255))
    date_created = Column(DateTime, nullable=False, default=func.now())
    remote_address = Column(String(255), nullable=False)
    process_time = Column(Numeric(precision=10,scale=6), nullable=False)


class LoggerMiddlewarePydanticModel(BaseModel):
    id:int
    status_code:int
    method:str
    url:str
    error_message:Optional[str]
    date_created:datetime
    process_time:float
    remote_address:str

