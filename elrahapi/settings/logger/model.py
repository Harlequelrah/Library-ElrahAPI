from app.settings.database.base import Base
from elrahapi.middleware.models import MetaLogModel
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship


class LogModel(Base, MetaLogModel):
    # USER_FK_NAME = "user_id"
    __tablename__ = "logs"
    # user_id:Mapped[int|None] = mapped_column(ForeignKey("users.id"))
    # user: Mapped["User"] = relationship( back_populates="user_logs")


# vous pouvez adapter  la classe selon vos besoin
