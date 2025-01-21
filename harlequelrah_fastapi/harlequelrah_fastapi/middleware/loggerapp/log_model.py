from myproject.settings.database import Base
from harlequelrah_fastapi.middleware.models import LoggerMiddlewareModel

class Logger(Base, LoggerMiddlewareModel):
    __tablename__ = "loggers"
