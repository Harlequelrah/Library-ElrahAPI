from decimal import Decimal
from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    DateTime,
)
from sqlalchemy.sql import func
from typing import List, Optional
from datetime import datetime


class Logger:
    id = Column(Integer, primary_key=True, index=True)
    status_code = Column(Integer, index=True)
    method = Column(String(30), nullable=False)
    url = Column(String(30), nullable=False)
    date_created = Column(DateTime, nullable=False, default=func.now())
    process_time = Column(Decimal, nullable=False)
    db_name = Column(String(30), nullable=False)
    user_agent = Column(String(36), nullable=False)
