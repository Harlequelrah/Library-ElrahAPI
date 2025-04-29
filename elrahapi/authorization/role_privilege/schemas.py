
from typing import Optional
from pydantic import BaseModel, Field

from elrahapi.authorization.base_meta_model import MetaAuthorizationBaseModel



class RolePrivilegeCreateModel(BaseModel):
    role_id : int = Field(example=1)
    privilege_id :int = Field(exemaple=2)

class RolePrivilegePatchModel(BaseModel):
    role_id : Optional[int] = Field(example=1,default=None)
    privilege :Optional[int] = Field(example=2,default=None)
class RolePrivilegeUpdateModel(BaseModel):
    role_id : int = Field(example=1)
    privilege_id :int = Field(example=2)

class RolePrivilegeReadModel(RolePrivilegeCreateModel):
    id : int
    class Config :
        from_attributes = True


class RolePrivilegeFullReadModel(BaseModel):
    id:int
    role : MetaAuthorizationBaseModel
    privilege : MetaAuthorizationBaseModel
    class Config:
        from_attributes = True

