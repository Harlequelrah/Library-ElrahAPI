from elrahapi.authorization.base_meta_model import MetaAuthorizationBaseModel
from elrahapi.utility.schemas import AdditionalSchemaFields
from pydantic import BaseModel, ConfigDict, Field


class RolePrivilegeCreateModel(BaseModel):
    role_id: int = Field(examples=[1])
    privilege_id: int = Field(examples=[2])
    is_active: bool = Field(examples=[True], default=True)


class RolePrivilegePatchModel(BaseModel):
    role_id: int | None = Field(examples=[1], default=None)
    privilege_id: int | None = Field(examples=[2], default=None)
    is_active: bool | None = Field(examples=[True], default=None)


class RolePrivilegeUpdateModel(BaseModel):
    role_id: int = Field(examples=[1])
    privilege_id: int = Field(examples=[2])
    is_active: bool = Field(examples=[True])


class RolePrivilegeReadModel(RolePrivilegeCreateModel, AdditionalSchemaFields):
    id: int
    model_config = ConfigDict(from_attributes=True)


class RolePrivilegeFullReadModel(BaseModel, AdditionalSchemaFields):
    id: int
    role: MetaAuthorizationBaseModel
    privilege: MetaAuthorizationBaseModel
    is_active: bool
    model_config = ConfigDict(from_attributes=True)
