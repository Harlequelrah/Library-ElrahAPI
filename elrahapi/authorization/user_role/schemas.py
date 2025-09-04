from pydantic import BaseModel, Field


from elrahapi.user.schemas import UserInUserRole

from elrahapi.authorization.base_meta_model import MetaAuthorizationBaseModel
from elrahapi.utility.schemas import AdditionalSchemaFields


class UserRoleCreateModel(BaseModel):
    user_id: int = Field(example=1)
    role_id: int = Field(example=2)
    is_active: bool = Field(exemple=True, default=True)


class UserRoleReadModel(UserRoleCreateModel, AdditionalSchemaFields):
    id: int


class UserRoleFullReadModel(BaseModel, AdditionalSchemaFields):
    id: int
    user: UserInUserRole
    role: MetaAuthorizationBaseModel
    is_active: bool


class UserRolePatchModel(BaseModel):
    user_id: int | None = Field(example=1, default=None)
    role_id: int | None = Field(example=2, default=None)
    is_active: bool | None = Field(exemple=True, default=None)


class UserRoleUpdateModel(BaseModel):
    user_id: int = Field(example=1)
    role_id: int = Field(example=2)
    is_active: bool = Field(exemple=True)
