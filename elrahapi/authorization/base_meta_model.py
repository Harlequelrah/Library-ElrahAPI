from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import validates
from datetime import datetime

from elrahapi.utility.models import AdditionalModelFields


class MetaAuthorization(AdditionalModelFields):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    description = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    @validates("name")
    def validate_name(self, key, value):
        return value.upper().strip() if value else None


class MetaAuthorizationBaseModel(BaseModel):
    is_active: bool
    name: str
    description: str


class MetaAuthorizationReadModel(MetaAuthorizationBaseModel):
    id: int
    date_created: datetime
    date_updated: datetime
    date_deleted: datetime | None = None
    is_deleted: bool
