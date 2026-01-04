# from datetime import datetime

# from myproject.settings.database import Base
# from sqlalchemy.orm import Mapped, mapped_column, relationship
# from sqlalchemy.sql import func


# class Entity(Base):
#     __tablename__ = "entities"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     date_created: Mapped[datetime] = mapped_column(default=func.now())
#     date_updated: Mapped[datetime] = mapped_column(
#         default=func.now(), onupdate=func.now()
#     )
#     is_deleted: Mapped[bool] = mapped_column(default=False)
#     date_deleted: Mapped[datetime] = mapped_column(default=None)
