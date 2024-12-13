from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Numeric
)
from sqlalchemy.sql import func



class LoggerMiddlewareModel:
    id = Column(Integer, primary_key=True, index=True)
    status_code = Column(Integer, index=True)
    method = Column(String(30), nullable=False)
    url = Column(String(255), nullable=False)
    date_created = Column(DateTime, nullable=False, default=func.now())
    process_time = Column(Numeric(precision=10,scale=6), nullable=False)
    user_agent = Column(String(255), nullable=False)
