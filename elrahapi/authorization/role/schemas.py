
from elrahapi.authorization.base_meta_model import (
    MetaAuthorizationBaseModel,
    MetaAuthorizationReadModel,
)
from pydantic import BaseModel, Field

from elrahapi.authorization.role.meta_models import MetaRoleUsers



class RoleBaseModel(BaseModel):
    name: str = Field(example="Admin")
    description: str = Field(example="allow to manage all the system")


class RoleCreateModel(RoleBaseModel):
    is_active: bool = Field(example=True, default=True)


class RoleUpdateModel(RoleBaseModel):
    is_active: bool = Field(example=True)

class RolePatchModel(BaseModel):
    name: str | None = Field(example="Admin", default=None)
    is_active: bool|None = Field(example=True, default=None)
    description: str | None = Field(example="allow to manage all the system", default=None)


class RoleReadModel(MetaAuthorizationReadModel):
    class Config:
        from_attributes = True


class RoleFullReadModel(MetaAuthorizationReadModel):
    role_privileges: list["MetaAuthorizationBaseModel"] = []
    role_users:list["MetaRoleUsers"]=[]

    class Config:
        from_attributes = True




