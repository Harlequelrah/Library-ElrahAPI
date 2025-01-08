from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import validates,relationship
from pydantic import BaseModel, Field
from typing import List, Optional
class RoleModel:
    id=Column(Integer, primary_key=True,index=True)
    name=Column(String(100),nullable=False)
    normalizedName=Column(String(100),nullable=False)


    @validates('name')
    def validate_name(self,key,value):
        self.normalizedName= value.upper().strip() if value else None



class RoleBaseModel(BaseModel):
    name : str = Field(example="Admin")

class RoleCreateModel(RoleBaseModel):
    pass

class RoleUpdateModel(BaseModel):
    name:Optional[str]=Field(example="Admin",default=None)

class RolePydanticModel(BaseModel):
    id:int
    name:str
    normalizedName:str
    class setting:
        from_orm=True
