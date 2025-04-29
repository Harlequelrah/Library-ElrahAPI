
from pydantic import BaseModel,Field
from typing import Optional

from elrahapi.user.schemas import UserBaseModel

from elrahapi.authorization.base_meta_model import MetaAuthorizationBaseModel




class UserRoleCreateModel(BaseModel):
    user_id: int = Field(example=1)
    role_id: int=Field(example=2)
    is_active: Optional[bool] = Field(exemple=True,default=True)


class UserRoleReadModel(UserRoleCreateModel):
    id : int


class UserRoleFullReadModel(BaseModel):
    id : int
    user : UserBaseModel
    role : MetaAuthorizationBaseModel
    is_active:bool

class UserRolePatchModel(BaseModel):
    user_id: Optional[int ]= Field(example=1,default=None)
    role_id: Optional[int]=Field(example=2,default=None)
    is_active: Optional[bool] = Field(exemple=True,default=None)


class UserRoleUpdateModel(BaseModel):
    user_id: int = Field(example=1)
    role_id: int=Field(example=2)
    is_active: bool = Field(exemple=True)



