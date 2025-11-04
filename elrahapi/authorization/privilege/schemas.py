from pydantic import BaseModel, ConfigDict, Field

from elrahapi.authorization.base_meta_model import (
    MetaAuthorizationReadModel,
    MetaAuthorizationBaseModel,
)

from elrahapi.authorization.privilege.meta_models import PrivilegeUserInPrivilege


class PrivilegeBaseModel(BaseModel):
    name: str = Field(examples=["can_add_privilege"])
    description: str = Field(examples=["allow privilege creation for privilege"])


class PrivilegeCreateModel(PrivilegeBaseModel):
    is_active: bool = Field(default=True, examples=[True])


class PrivilegeUpdateModel(PrivilegeBaseModel):
    is_active: bool = Field(examples=[True])


class PrivilegePatchModel(BaseModel):
    name: str | None = Field(examples=["can_add_privilege"], default=None)
    is_active: bool | None = Field(default=None, examples=[True])
    description: str | None = Field(
        examples=["allow privilege creation for privilege"], default=None
    )


class PrivilegeReadModel(MetaAuthorizationReadModel):
    model_config = ConfigDict(from_attributes=True)


class PrivilegeFullReadModel(MetaAuthorizationReadModel):
    privilege_roles: list["MetaAuthorizationBaseModel"] | None = []
    privilege_users: list["PrivilegeUserInPrivilege"] | None = []
    model_config = ConfigDict(from_attributes=True)
