from sqlalchemy import Column, ForeignKey, Integer

from sqlalchemy.orm import relationship
from elrahapi.middleware.models import MetaLogModel
from sqlalchemy.ext.declarative import declarative_base
base = declarative_base()
class LogModel(base, MetaLogModel):
    # USER_FK_NAME = "user_id"
    __tablename__ = "logs"
    # user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    # user = relationship("User", back_populates="user_logs")


# vous pouvez adapter à la classe selon vos besoin

