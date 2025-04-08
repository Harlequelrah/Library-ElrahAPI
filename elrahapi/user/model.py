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
from sqlalchemy.orm import validates
from typing import List
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

    @validates('password')
    def validate_password(self, key, password):
        if not password or len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        try:
            return self.PasswordHasher.hash(password)
        except Exception as e:
            print(f"Error while setting password: {e}")


    MAX_ATTEMPT_LOGIN = None
    PasswordHasher = PasswordHasher()

    def try_login(self, is_success: bool):
        if is_success:
            self.attempt_login = 0
        else:
            self.attempt_login += 1
        if  self.MAX_ATTEMPT_LOGIN and self.attempt_login >= self.MAX_ATTEMPT_LOGIN:
            self.is_active = False




    def check_password(self, password: str) -> bool:
        try:
            self.PasswordHasher.verify(self.password, password)
            return True
        except Ex.VerifyMismatchError:
            print(self.password, password)
            return False
        except Ex.InvalidHashError:
            self.password=self.password
            return self.check_password(password)

    # def has_authorization(self):

    def has_role(self, role_name:str):
        for user_role in  self.user_roles :
            role=user_role.role
            if user_role.is_active and role.is_active and role.normalizedName == role_name.upper():
                return True
        else:
            raise INSUFICIENT_PERMISSIONS_CUSTOM_HTTP_EXCEPTION


    def has_permission(self,privilege_name:str):
        for user_privilege in self.user_privileges:
            privilege = user_privilege.privilege
            if user_privilege.is_active and privilege.is_active and privilege.normalizedName == privilege_name.upper():
                    return True
        else : return False


    def has_privilege(self, privilege_name: str):
        for user_role in self.user_roles:
            for user_privilege in user_role.role.role_privileges:
                privilege=user_privilege.privilege
                if (privilege.normalizedName==privilege_name.upper() and privilege.is_active and user_privilege.is_active):
                    return True
        if self.has_permission(privilege_name=privilege_name):
            return True
        else:
            raise INSUFICIENT_PERMISSIONS_CUSTOM_HTTP_EXCEPTION





