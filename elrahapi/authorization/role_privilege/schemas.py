from typing import Optional
from pydantic import BaseModel, Field

from elrahapi.authorization.base_meta_model import MetaAuthorizationBaseModel


class RolePrivilegeCreateModel(BaseModel):
    role_id : int = Field(example=1)
    privilege_id :int = Field(example=2)
    is_active: Optional[bool] = Field(exemple=True, default=True)


class RolePrivilegePatchModel(BaseModel):
    role_id : Optional[int] = Field(example=1,default=None)
    privilege_id :Optional[int] = Field(example=2,default=None)
    is_active: Optional[bool] = Field(exemple=True, default=None)

class RolePrivilegeUpdateModel(BaseModel):
    role_id : int = Field(example=1)
    privilege_id :int = Field(example=2)
    is_active: bool = Field(exemple=True)
class RolePrivilegeReadModel(RolePrivilegeCreateModel):
    id : int
    class Config :
        from_attributes = True


class RolePrivilegeFullReadModel(BaseModel):
    id:int
    role : MetaAuthorizationBaseModel
    privilege : MetaAuthorizationBaseModel
    is_active:bool
    class Config:
        from_attributes = True
