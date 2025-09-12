from sqlalchemy import Boolean, Column, DateTime, func


class AdditionalModelFields:
    date_created = Column(DateTime, default=func.now())
    date_updated = Column(DateTime, default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False, nullable=False)
    date_deleted = Column(DateTime, nullable=True)
