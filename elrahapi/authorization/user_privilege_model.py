
from pydantic import BaseModel,Field
from typing import Optional

from sqlalchemy import Boolean, Column, ForeignKey, Integer



class UserPrivilegeModel:
    id = Column(Integer, primary_key=True,index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    privilege_id = Column(Integer, ForeignKey("privileges.id"))
    is_active = Column(Boolean, default=True)

class UserPrivilegeCreateModel(BaseModel):
    user_id: int = Field(example=1)
    privilege_id: int=Field(example=2)
    is_active: Optional[bool] = Field(exemple=True,default=True)


class UserPrivilegePydanticModel(UserPrivilegeCreateModel):
    id : int
    class Config:
        from_attributes=True

class UserPrivilegePatchModel(BaseModel):
    user_id: Optional[int ]= Field(example=1,default=None)
    privilege_id: Optional[int]=Field(example=2,default=None)
    is_active: Optional[bool] = Field(exemple=True,default=None)


class UserPrivilegeUpdateModel(BaseModel):
    user_id: int = Field(example=1)
    privilege_id: int=Field(example=2)
    is_active: bool = Field(exemple=True)



