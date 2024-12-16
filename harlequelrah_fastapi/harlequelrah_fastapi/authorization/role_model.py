from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import validates
from pydantic import BaseModel, Field
from typing import List, Optional

class Role():
    id=Column(Integer, primary_key=True,index=True)
    name=Column(String(100),nullable=False)
    normalizedName=Column(String(100),nullable=False)

    @validates('name')
    def validate_name(self,key,value):
        self.normalizedName= value.upper() if value else None



class RoleBaseModel(BaseModel):
    name : str = Field(example="Admin")

class RoleCreate(RoleBaseModel):
    pass

class RoleUpdate(BaseModel):
    name:Optional[str]=Field(example="Admin",default=None)

class Role(RoleCreate):
    id:int
    normalizedName:str
    class setting:
        from_orm=True
