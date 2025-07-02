from ..database import database
from elrahapi.middleware.models import LogModel


class Log(database.base, LogModel):
    __tablename__ = "logs"


metadata = database.base.metadata
