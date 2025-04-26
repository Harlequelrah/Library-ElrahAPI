
from pydantic import BaseModel,Field
from typing import Optional

from sqlalchemy import Boolean, Column, ForeignKey, Integer

from elrahapi.authorization.meta_model import MetaAuthorizationBaseModel

from elrahapi.user.schemas import UserBaseModel



class UserPrivilegeModel:
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    privilege_id = Column(Integer, ForeignKey("privileges.id"),nullable=False)
    is_active = Column(Boolean, default=True)

class UserPrivilegeCreateModel(BaseModel):
    user_id: int = Field(example=1)
    privilege_id: int=Field(example=2)
    is_active: Optional[bool] = Field(exemple=True,default=True)


class UserPrivilegeReadModel(UserPrivilegeCreateModel):
    id : int
    class Config:
        from_attributes=True


class UserPrivilegeFullReadModel(BaseModel):
    id:int
    user: UserBaseModel
    privilege:MetaAuthorizationBaseModel
    is_active:bool
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



