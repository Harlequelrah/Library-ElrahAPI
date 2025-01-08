from typing import Optional
from pydantic import BaseModel, Field
from sqlalchemy import Boolean, Column, ForeignKey, Integer,String
from sqlalchemy.orm import validates,Session,relationship


class PrivilegeModel:
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(50),unique=True)
    normalizedName=Column(String(50),unique=True)
    description=Column(String(255),nullable=False)
    is_active=Column(Boolean,default=True)

    validates('name')
    def validate_name(self,key,value):
        if value is not None:
            self.normalizedName= value.upper().strip()

class PrivilegeBaseModel(BaseModel):
    name : str=Field(example='can_add_privilege')

class PrivilegeCreateModel(PrivilegeBaseModel):
    description:str=Field(example='allow privilege creation for privilege')
    role_id:int=Field(example=1)


class PrivilegeUpdateModel(BaseModel):
    name: Optional[str] = Field(example="can_add_privilege")
    is_active:Optional[bool]=Field(default=True,example=True)
    role_id:Optional[int]=Field(example=1)


class PrivilegePydanticModel(BaseModel):
    id:int
    name:str
    normalizedName:str
    description: str
    is_active:bool
    role_id:int
    class config :
        from_orm=True

class MetaPrivilege(BaseModel):
    id:int
    normalizedName:str
    description: str
    is_active: bool
