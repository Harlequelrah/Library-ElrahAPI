from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    DateTime,
)
from sqlalchemy.sql import func
from argon2 import PasswordHasher, exceptions as Ex
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class User:
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(256), unique=True, index=True)
    username = Column(String(256), unique=True, index=True)
    password = Column(String(1024), nullable=False)
    lastname = Column(String(256), nullable=False)
    firstname = Column(String(256), nullable=False)
    date_created = Column(DateTime, nullable=False, default=func.now())
    date_updated = Column(DateTime, onupdate=func.now())
    is_active = Column(Boolean, default=True)
    attempt_login = Column(Integer, default=0)

    MAX_ATTEMPT_LOGIN = 3

    def __init__(self):
        self.PasswordHasher = PasswordHasher()

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


class UserBaseModel(BaseModel):
    email: str = Field(example="user@example.com")
    username: str = Field(example="Harlequelrah")
    lastname: str = Field(example="SMITH")
    firstname: str = Field(example="jean-francois")


class UserCreateModel(UserBaseModel):
    password: str = Field(example="m*td*pa**e")


class UserUpdateModel(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    lastname: Optional[str] = None
    firstname: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None


class UserPydanticModel(UserBaseModel):
    id: int
    is_active: bool
    date_created: datetime
    date_updated: datetime


class UserLoginRequestModel(BaseModel):
    username: Optional[str] = None
    password: str
    email: Optional[str] = None


class UserChangePasswordRequestModel(UserLoginRequestModel):
    current_password: str
    new_password: str
