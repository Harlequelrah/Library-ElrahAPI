from sqlalchemy import (
    Integer,
    String,
    DateTime,
    Boolean,
    Column,
    ForeignKey,
)
from sqlalchemy.sql import func
from argon2 import PasswordHasher, exceptions as Ex
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from elrahapi.authorization.meta_model import MetaAuthorizationBaseModel, MetaUserPrivilegeModel
from elrahapi.exception.auth_exception  import INSUFICIENT_PERMISSIONS_CUSTOM_HTTP_EXCEPTION


class UserModel:
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(256), unique=True, index=True)
    username = Column(String(256), unique=True, index=True)
    password = Column(String(1024), nullable=False)
    lastname = Column(String(256), nullable=False)
    firstname = Column(String(256), nullable=False)
    date_created = Column(DateTime,  default=func.now())
    date_updated = Column(DateTime, onupdate=func.now())
    is_active = Column(Boolean, default=True)
    attempt_login = Column(Integer, default=0)
    role_id = Column(Integer, ForeignKey("roles.id"))




    MAX_ATTEMPT_LOGIN = 3
    PasswordHasher = PasswordHasher()

    def try_login(self, is_success: bool):
        if is_success:
            self.attempt_login = 0
        else:
            self.attempt_login += 1
        if self.attempt_login >= self.MAX_ATTEMPT_LOGIN:
            self.is_active = False

    def set_password(self, password: str):
        self.password = self.PasswordHasher.hash(password)

    def check_password(self, password: str) -> bool:
        try:
            self.PasswordHasher.verify(self.password, password)
            return True
        except Ex.VerifyMismatchError:
            return False
        except Ex.InvalidHashError:
            self.set_password(password)
            return self.check_password(password)


    def has_role(self, roles_name: List[str]):
        for role_name in roles_name :
            if self.role and role_name.upper() == self.role.normalizedName and self.role.is_active:
                return True
        else:
            raise INSUFICIENT_PERMISSIONS_CUSTOM_HTTP_EXCEPTION

    def has_privilege(self, privilege_name: str):
        if self.role:
            role_privileges=self.role.role_privileges
            for role_privilege in role_privileges :
                privilege=role_privilege.privilege
                if (privilege.normalizedName==privilege_name.upper() and privilege.is_active):
                    return True
        for user_privilege in self.user_privileges:
            if user_privilege.is_active:
                privilege = user_privilege.privilege
                if (
                    privilege.normalizedName == privilege_name.upper()
                    and privilege.is_active
                ):
                    return True
        else : raise INSUFICIENT_PERMISSIONS_CUSTOM_HTTP_EXCEPTION



class UserBaseModel(BaseModel):
    email: str = Field(example="user@example.com")
    username: str = Field(example="Harlequelrah")
    lastname: str = Field(example="SMITH")
    firstname: str = Field(example="jean-francois")


class UserCreateModel(UserBaseModel):
    password: str = Field(example="m*td*pa**e")
    role_id : Optional[int] = Field(example=1,default=None)



class UserPatchModel(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    lastname: Optional[str] = None
    firstname: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None
    role_id : Optional[int] = None

class UserUpdateModel(BaseModel):
    email: str
    username: str
    lastname: str
    firstname: str
    is_active: bool
    password: str
    role_id : int

class UserPydanticModel(UserBaseModel):
    id: int
    is_active: bool
    attempt_login:int
    date_created: datetime
    date_updated: Optional[datetime]
    role : Optional[MetaAuthorizationBaseModel]
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


