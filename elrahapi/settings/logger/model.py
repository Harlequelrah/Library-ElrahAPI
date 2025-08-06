from sqlalchemy import Column, ForeignKey, Integer

from sqlalchemy.orm import relationship
from elrahapi.middleware.models import MetaLogModel

class LogModel(Base, MetaLogModel):
    # USER_FK_NAME = "user_id"
    __tablename__ = "logs"
    # user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    # user = relationship("User", back_populates="user_logs")


# vous pouvez adapter à la classe selon vos besoin

