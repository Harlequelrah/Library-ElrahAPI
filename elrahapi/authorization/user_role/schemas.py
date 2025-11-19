from elrahapi.authorization.base_meta_model import MetaAuthorizationBaseModel
from elrahapi.user.schemas import UserInUserRole
from elrahapi.utility.schemas import AdditionalSchemaFields
from pydantic import BaseModel, Field


class UserRoleCreateModel(BaseModel):
    user_id: int = Field(examples=[1])
    role_id: int = Field(examples=[2])
    is_active: bool = Field(examples=[True], default=True)


class UserRoleReadModel(UserRoleCreateModel, AdditionalSchemaFields):
    id: int


class UserRoleFullReadModel(BaseModel, AdditionalSchemaFields):
    id: int
    user: UserInUserRole
    role: MetaAuthorizationBaseModel
    is_active: bool


class UserRolePatchModel(BaseModel):
    user_id: int | None = Field(examples=[1], default=None)
    role_id: int | None = Field(examples=[2], default=None)
    is_active: bool | None = Field(examples=[True], default=None)


class UserRoleUpdateModel(BaseModel):
    user_id: int = Field(examples=[1])
    role_id: int = Field(examples=[2])
    is_active: bool = Field(examples=[True])
