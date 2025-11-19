from pydantic import BaseModel, Field, EmailStr, field_validator

from elrahapi.authorization.user_role.meta_models import UserRoleInUser

from elrahapi.authorization.user_privilege.meta_models import UserPrivilegeInUser
from elrahapi.utility.schemas import AdditionalSchemaFields


class UserBaseModel(BaseModel):
    email: EmailStr = Field(examples=["user@example.com"])
    username: str = Field(examples=["Harlequelrah"])
    lastname: str = Field(examples=["SMITH"])
    firstname: str = Field(examples=["jean-francois"])


class UserCreateModel:
    password: str = Field(examples=["m*td*pa**e"])


class UserPatchModel:
    email: EmailStr | None = Field(examples=["user@example.com"], default=None)
    username: str | None = Field(examples=["Harlequelrah"], default=None)
    lastname: str | None = Field(examples=["SMITH"], default=None)
    firstname: str | None = Field(examples=["jean-francois"], default=None)


class UserUpdateModel:
    pass


class UserReadModel(AdditionalSchemaFields):
    id: int
    is_active: bool
    attempt_login: int


class UserFullReadModel(UserReadModel):
    user_roles: list["UserRoleInUser"] = []
    user_privileges: list["UserPrivilegeInUser"] = []


class UserRequestModel(BaseModel):
    username: str | None = None
    email: str | None = None

    @property
    def sub(self):
        return self.username or self.email

    @field_validator("sub", check_fields=False)
    @classmethod
    def validate_sub(cls, value):
        if not value:
            raise ValueError("username or email must be provided")
        return value


class UserLoginRequestModel(UserRequestModel):
    password: str


class UserChangePasswordRequestModel(UserRequestModel):
    current_password: str
    new_password: str


class UserInPrivilegeUser(UserBaseModel):
    is_active: bool


class UserInRoleUser(UserBaseModel):
    is_active: bool


class UserInUserPrivilege(UserBaseModel):
    is_active: bool


class UserInUserRole(UserBaseModel):
    is_active: bool
