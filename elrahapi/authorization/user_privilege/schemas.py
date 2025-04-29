

from pydantic import BaseModel,Field
from typing import Optional

from elrahapi.authorization.base_meta_model import MetaAuthorizationBaseModel

from elrahapi.user.schemas import UserBaseModel

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



