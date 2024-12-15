from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    DateTime,
)
from sqlalchemy.sql import func
from argon2 import PasswordHasher, exceptions as Ex
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Role():
    id=Column(Integer, primary_key=True,index=True)
    name=Column(String(100),nullable=False)
    normalizedName=Column(String(100),nullable=False)


class RoleBaseModel(BaseModel):
    name : str = Field(example="Admin")
    normalizedName : str = Field(example="ADMIN")

class RoleCreate(RoleBaseModel):
    pass

class RoleUpdate(RoleBaseModel):
    name:Optional[str]=Field(example="Admin",default=None)
    normalizedName:Optional[str]=Field(example="ADMIN",default=None)

class Role(RoleCreate):
    id:int
    class setting:
        from_orm=True
