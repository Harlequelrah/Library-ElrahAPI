from ..database import Base
from elrahapi.middleware.models import LoggerMiddlewareModel

class Logger(Base, LoggerMiddlewareModel):
    __tablename__ = "loggers"
metadata = Base.metadata
