from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Numeric,
    Text
)
from pydantic import BaseModel
from datetime import datetime

from sqlalchemy.sql import func


class MetaLogModel:
    id = Column(Integer, primary_key=True)
    status_code = Column(Integer, index=True)
    method = Column(String(30), nullable=False)
    url = Column(String(255), nullable=False)
    error_message=Column(Text)
    date_created = Column(DateTime, nullable=False, default=func.now())
    remote_address = Column(String(255), nullable=False)
    process_time = Column(Numeric(precision=10,scale=6), nullable=False)




class MetaLogReadModel(BaseModel):
    id:int
    status_code:int
    method:str
    url:str
    error_message:str | None = None
    date_created:datetime
    process_time:float
    remote_address:str
