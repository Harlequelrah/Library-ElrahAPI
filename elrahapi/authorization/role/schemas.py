from elrahapi.authorization.base_meta_model import (
    MetaAuthorizationBaseModel,
    MetaAuthorizationReadModel,
)
from pydantic import BaseModel, ConfigDict, Field
from elrahapi.authorization.role.meta_models import RoleUserInRole


class RoleBaseModel(BaseModel):
    name: str = Field(examples=["Admin"])
    description: str = Field(examples=["allow to manage all the system"])


class RoleCreateModel(RoleBaseModel):
    is_active: bool = Field(examples=[True], default=True)


class RoleUpdateModel(RoleBaseModel):
    is_active: bool = Field(examples=[True])


class RolePatchModel(BaseModel):
    name: str | None = Field(examples=["Admin"], default=None)
    is_active: bool | None = Field(examples=[True], default=None)
    description: str | None = Field(
        examples=["allow to manage all the system"], default=None
    )

class RoleReadModel(MetaAuthorizationReadModel):
    model_config = ConfigDict(from_attributes=True)


class RoleFullReadModel(MetaAuthorizationReadModel):
    role_privileges: list["MetaAuthorizationBaseModel"] = []
    role_users: list["RoleUserInRole"] = []

    model_config = ConfigDict(from_attributes=True)
