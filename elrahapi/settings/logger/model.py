from ..database import Base
from elrahapi.middleware.models import LogModel

class Log(Base, LogModel):
    __tablename__ = "logs"
metadata = Base.metadata
