from sqlalchemy import Column, ForeignKey, Integer

from elrahapi.router import relationship
from ..database import database
from elrahapi.middleware.models import MetaLogModel


class LogModel(database.base, MetaLogModel):
    __tablename__ = "logs"
    # user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    # user = relationship("User",back_populates="user_logs")


# vous pouvez adapter user_id et user  pour qu'elle corresponde à votre modèle de données
# vous devez cependant garder le nom de colonne user_id
metadata = database.base.metadata
