from sqlalchemy import Column, ForeignKey, Integer
from ..database import database
from elrahapi.middleware.models import MetaLogModel

class LogModel(database.base, MetaLogModel):
    __tablename__ = "logs"
    # subject = Column(Integer, ForeignKey("users.id"), nullable=True)

# vous pouvez adapter à votre cas la colonne subject pour qu'elle corresponde à votre modèle de données
metadata = database.base.metadata
