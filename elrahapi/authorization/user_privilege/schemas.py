from pydantic import BaseModel, ConfigDict, Field


from elrahapi.authorization.base_meta_model import MetaAuthorizationBaseModel

from elrahapi.user.schemas import UserInUserPrivilege
from elrahapi.utility.schemas import AdditionalSchemaFields


class UserPrivilegeCreateModel(BaseModel):
    user_id: int = Field(example=1)
    privilege_id: int = Field(example=2)
    is_active: bool = Field(exemple=True, default=True)


class UserPrivilegeReadModel(UserPrivilegeCreateModel, AdditionalSchemaFields):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserPrivilegeFullReadModel(BaseModel, AdditionalSchemaFields):
    id: int
    user: UserInUserPrivilege
    privilege: MetaAuthorizationBaseModel
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class UserPrivilegePatchModel(BaseModel):
    user_id: int | None = Field(example=1, default=None)
    privilege_id: int | None = Field(example=2, default=None)
    is_active: bool | None = Field(exemple=True, default=None)


class UserPrivilegeUpdateModel(BaseModel):
    user_id: int = Field(example=1)
    privilege_id: int = Field(example=2)
    is_active: bool = Field(exemple=True)
