from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
)
from harlequelrah_fastapi.authorization.privilege_model import MetaPrivilege
from sqlalchemy.sql import func
from sqlalchemy.orm import validates, relationship
from pydantic import BaseModel, Field
from typing import List, Optional


class RoleModel:
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    normalizedName = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)

    @validates("name")
    def validate_name(self, key, value):
        self.normalizedName = value.upper().strip() if value else None


class RoleBaseModel(BaseModel):
    name: str = Field(example="Admin")


class RoleCreateModel(RoleBaseModel):
    pass


class RoleUpdateModel(BaseModel):
    name: Optional[str] = Field(example="Admin", default=None)
    is_active : Optional[bool] = Field(example=True, default=None)


class RolePydanticModel(BaseModel):
    id: int
    name: str
    normalizedName: str
    is_active: bool
    privileges: List[MetaPrivilege]

    class Config:
        from_orm = True
