from pydantic import BaseModel, Field,EmailStr
from typing import List, Optional
from datetime import datetime
from elrahapi.authorization.meta_model import  MetaUserPrivilegeModel,MetaUserRoleModel

class UserBaseModel(BaseModel):
    email: EmailStr = Field(example="user@example.com")
    username: str = Field(example="Harlequelrah")
    lastname: str = Field(example="SMITH")
    firstname: str = Field(example="jean-francois")


class UserCreateModel(UserBaseModel):
    password: str = Field(example="m*td*pa**e")



class UserPatchModel(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    lastname: Optional[str] = None
    firstname: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None

class UserUpdateModel(BaseModel):
    email: EmailStr
    username: str
    lastname: str
    firstname: str
    is_active: bool
    password: str

class UserPydanticModel(UserBaseModel):
    id: int
    is_active: bool
    attempt_login:int
    date_created: datetime
    date_updated: Optional[datetime]
    user_roles:Optional[List["MetaUserRoleModel"]]
    user_privileges: Optional[List["MetaUserPrivilegeModel"]]






class UserRequestModel(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    @property
    def username_or_email(self):
        return self.username or self.email
class UserLoginRequestModel(UserRequestModel):
    password: str



class UserChangePasswordRequestModel(UserRequestModel):
    current_password: str
    new_password: str
