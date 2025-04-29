
from elrahapi.authorization.base_meta_model import (
    MetaAuthorizationBaseModel,
    MetaAuthorizationReadModel,
)
from pydantic import BaseModel, Field
from typing import List, Optional

from elrahapi.authorization.role.meta_models import MetaRoleUsers



class RoleBaseModel(BaseModel):
    name: str = Field(example="Admin")
    description: str = Field(example="allow to manage all the system")


class RoleCreateModel(RoleBaseModel):
    is_active: Optional[bool] = Field(example=True, default=True)


class RoleUpdateModel(RoleBaseModel):
    is_active: bool = Field(example=True)

class RolePatchModel(BaseModel):
    name: Optional[str] = Field(example="Admin", default=None)
    is_active: Optional[bool] = Field(example=True, default=None)
    description: Optional[str] = Field(example="allow to manage all the system", default=None)


class RoleReadModel(MetaAuthorizationReadModel):
    class Config:
        from_attributes = True


class RoleFullReadModel(MetaAuthorizationReadModel):
    role_privileges: List["MetaAuthorizationBaseModel"] = []
    role_users:List["MetaRoleUsers"]=[]

    class Config:
        from_attributes = True




