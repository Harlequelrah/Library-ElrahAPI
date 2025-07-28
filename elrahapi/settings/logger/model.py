from ..database import database
from elrahapi.middleware.models import MetaLogModel

class LogModel(database.base, MetaLogModel):
    __tablename__ = "logs"


metadata = database.base.metadata
