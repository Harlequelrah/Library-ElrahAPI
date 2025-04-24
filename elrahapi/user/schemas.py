from pydantic import BaseModel, Field,EmailStr
from typing import List, Optional
from datetime import datetime
from elrahapi.authorization.meta_model import  MetaUserPrivilegeModel,MetaUserRoleModel

class UserBaseModel:
    email: EmailStr = Field(example="user@example.com")
    username: str = Field(example="Harlequelrah")
    lastname: str = Field(example="SMITH")
    firstname: str = Field(example="jean-francois")


class UserCreateModel:
    password: str = Field(example="m*td*pa**e")



class UserPatchModel:
    email: Optional[EmailStr] = Field(example="user@example.com",default=None)
    username: Optional[str] = Field(example="Harlequelrah",default=None)
    lastname: Optional[str] = Field(example="SMITH",default=None)
    firstname: Optional[str] = Field(example="jean-francois",default=None)
    is_active: Optional[bool] = Field(example=True,default=None)
    password: Optional[str] = Field(example="m*td*pa**e",default=None)

class UserUpdateModel(UserCreateModel):
    is_active: bool = Field(example=True)

class UserPydanticModel:
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
