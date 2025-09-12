from argon2 import PasswordHasher
from argon2 import exceptions as Ex
from elrahapi.authentication.authentication_manager import AuthenticationManager
from elrahapi.exception.auth_exception import (
    INSUFICIENT_PERMISSIONS_CUSTOM_HTTP_EXCEPTION,
)
from elrahapi.exception.exceptions_utils import raise_custom_http_exception
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import validates
from sqlalchemy.sql import func

from fastapi import status

from elrahapi.utility.models import AdditionalModelFields


class UserModel(AdditionalModelFields):
    id = Column(Integer, primary_key=True)
    email = Column(String(256), unique=True, index=True)
    username = Column(String(256), unique=True, index=True)
    password = Column(String(1024), nullable=False)
    lastname = Column(String(256), nullable=False)
    firstname = Column(String(256), nullable=False)
    is_active = Column(Boolean, default=True)
    attempt_login = Column(Integer, default=0)

    @validates("password")
    def validate_password(self, key, password):
        if not password or len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        try:
            return self.PasswordHasher.hash(password)
        except Exception as e:
            detail = f"Error while setting password: {e}"
            raise_custom_http_exception(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=detail,
            )

    MAX_ATTEMPT_LOGIN = None
    PasswordHasher = PasswordHasher()

    def build_access_token_data(self, authentication: AuthenticationManager):
        pk_name = authentication.authentication_models.primary_key_name
        data = {
            "sub": str(getattr(self, pk_name)),
            "roles": [
                user_role.role.name
                for user_role in self.user_roles
                if user_role.is_active and user_role.role.is_active
            ],
        }
        return data

    def build_refresh_token_data(self, authentication: AuthenticationManager):
        pk_name = authentication.authentication_models.primary_key_name
        data = {
            "sub": str(getattr(self, pk_name)),
        }
        return data

    def build_temp_token_data(self, authentication: AuthenticationManager):
        pk_name = authentication.authentication_models.primary_key_name
        data = {
            "sub": str(getattr(self, pk_name)),
        }
        return data

    def try_login(self, is_success: bool):
        if is_success:
            self.attempt_login = 0
        else:
            self.attempt_login += 1
        if self.MAX_ATTEMPT_LOGIN and self.attempt_login >= self.MAX_ATTEMPT_LOGIN:
            self.is_active = False

    def change_user_state(self):
        self.is_active = not self.is_active

    def check_password(self, password: str) -> bool:
        try:
            self.PasswordHasher.verify(self.password, password)
            return True
        except Ex.VerifyMismatchError:
            return False
        except Ex.InvalidHashError:
            self.password = self.password
            return self.check_password(password)

    def has_role(self, role_name: str):
        for user_role in self.user_roles:
            role = user_role.role
            if (
                user_role.is_active
                and role.is_active
                and not role.is_deleted
                and not user_role.is_deleted
                and role.name == role_name.upper()
            ):
                return True
        else:
            raise INSUFICIENT_PERMISSIONS_CUSTOM_HTTP_EXCEPTION

    def has_permission(self, privilege_name: str):
        for user_privilege in self.user_privileges:
            privilege = user_privilege.privilege
            if (
                user_privilege.is_active
                and not user_privilege.is_deleted
                and privilege.is_active
                and privilege.name == privilege_name.upper()
                and not privilege.is_deleted
            ):
                return True
        else:
            return False

    def has_privilege(self, privilege_name: str):
        for user_role in self.user_roles:
            if user_role.is_active and not user_role.is_deleted:
                for user_privilege in user_role.role.role_privileges:
                    privilege = user_privilege.privilege
                    if (
                        privilege.name == privilege_name.upper()
                        and privilege.is_active
                        and not privilege.is_deleted
                        and user_privilege.is_active
                        and not user_privilege.is_deleted
                    ):
                        return True
        if self.has_permission(privilege_name=privilege_name):
            return True
        else:
            raise INSUFICIENT_PERMISSIONS_CUSTOM_HTTP_EXCEPTION
