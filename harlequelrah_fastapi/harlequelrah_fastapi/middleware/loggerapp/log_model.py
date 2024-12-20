from settings.database import Base
from harlequelrah_fastapi.middleware.model import LoggerMiddlewareModel

class Logger(Base, LoggerMiddlewareModel):
    __tablename__ = "loggers"
