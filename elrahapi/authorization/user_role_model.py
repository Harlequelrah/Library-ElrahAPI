
from pydantic import BaseModel,Field
from typing import Optional

from sqlalchemy import Boolean, Column, ForeignKey, Integer



class UserRoleModel:
    id = Column(Integer, primary_key=True , index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role_id = Column(Integer, ForeignKey("roles.id"))
    is_active = Column(Boolean, default=True)

class UserRoleCreateModel(BaseModel):
    user_id: int = Field(example=1)
    role_id: int=Field(example=2)
    is_active: Optional[bool] = Field(exemple=True,default=True)


class UserRolePydanticModel(UserRoleCreateModel):
    id : int
    class Config:
        from_attributes=True

class UserRolePatchModel(BaseModel):
    user_id: Optional[int ]= Field(example=1,default=None)
    role_id: Optional[int]=Field(example=2,default=None)
    is_active: Optional[bool] = Field(exemple=True,default=None)


class UserRoleUpdateModel(BaseModel):
    user_id: int = Field(example=1)
    role_id: int=Field(example=2)
    is_active: bool = Field(exemple=True)



