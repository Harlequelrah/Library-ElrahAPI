from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


class AdditionalModelFields:
    date_created: Mapped[datetime] = mapped_column(default=func.now())
    date_updated: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )
    is_deleted: Mapped[bool] = mapped_column(default=False)
    date_deleted: Mapped[datetime | None] = mapped_column(default=None)
