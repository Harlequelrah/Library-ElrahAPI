
from typing import Optional
from pydantic import BaseModel
from pydantic import BaseModel, Field
from sqlalchemy import Column,Integer,ForeignKey


class RolePrivilegeModel:
    id=Column(Integer,primary_key=True)
    role_id = Column(Integer,ForeignKey('roles.id'))
    privilege_id = Column(Integer,ForeignKey('privileges.id'))

class RolePrivilegeCreateModel(BaseModel):
    role_id : int = Field(example=1)
    privilege_id :int = Field(exemaple=2)

class RolePrivilegePatchModel(BaseModel):
    role_id : Optional[int] = Field(example=1,default=None)
    privilege :Optional[int] = Field(example=2,default=None)
class RolePrivilegeUpdateModel(BaseModel):
    role_id : int = Field(example=1)
    privilege :int = Field(example=2)

class RolePrivilegePydanticModel(RolePrivilegeCreateModel):
    id : int
    class Config :
        from_attributes = True



