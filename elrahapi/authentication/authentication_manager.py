

from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import Depends,status
from elrahapi.authentication.authentication_provider import OAUTH2_SCHEME, Authentication, AuthenticationProvider
from sqlalchemy.orm import Session
from sqlalchemy import or_
from elrahapi.authentication.token import RefreshToken
from elrahapi.crud.crud_models import CrudModels
from elrahapi.exception.auth_exception import INACTIVE_USER_CUSTOM_HTTP_EXCEPTION, INSUFICIENT_PERMISSIONS_CUSTOM_HTTP_EXCEPTION, INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION
from elrahapi.exception.exceptions_utils import raise_custom_http_exception
from elrahapi.user.models import (
    UserPydanticModel,
    UserCreateModel,
    UserUpdateModel,
    UserPatchModel,
    UserModel as User,
)
USER_AUTH_MODELS = CrudModels(
        UserPydanticModel=UserPydanticModel,
        UserSQLAlchemyModel=User,
        UserCreateModel=UserCreateModel,
        UserUpdateModel=UserUpdateModel,
        UserPatchModel=UserPatchModel,
)
class Authentication:
    def __init__(self, authentication_provider:AuthenticationProvider,crud_model:Optional[CrudModels]=USER_AUTH_MODELS):
        self.crud_model = crud_model
        self.authentication_provider = authentication_provider
        self.sqlalchemy_model = self.crud_model.sqlalchemy_model

    async def get_user_by_sub(self, username_or_email: str, db: Session):

        user = (
            db.query(self.sqlalchemy_model)
            .filter(
                or_(
                    self.sqlalchemy.username == username_or_email,
                    self.sqlalchemy.email == username_or_email,
                )
            )
            .first()
        )
        if user is None:
            raise INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION
        return user

    def check_authorization(
        self,
        privilege_name: Optional[List[str]] = None,
        roles_name: Optional[List[str]] = None,
    ) -> callable:
        async def is_authorized(token: str = Depends(self.authentication_provider.get_access_token)) -> bool:
            payload = await self.authentication_provider.validate_token(token)
            sub = payload.get("sub")
            db = self.authentication_provider.get_session()
            user = await self.get_user_by_sub(username_or_email=sub, db=db)
            if not user:
                raise_custom_http_exception(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found"
                )
            if roles_name:
                return user.has_role(roles_name)
            elif privilege_name:
                return user.has_privilege(privilege_name)
            else:
                raise INSUFICIENT_PERMISSIONS_CUSTOM_HTTP_EXCEPTION

        return is_authorized

    async def authenticate_user(
        self,
        password: str,
        username_or_email: Optional[str] = None,
        session: Optional[Session] = None,
    ):
        if username_or_email is None:
            raise INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION
        db = session if session else self.authentication_provider.get_session()
        user = await self.get_user_by_sub(db=db, username_or_email=username_or_email)
        if user:
            if not user.check_password(password):
                user.try_login(False)
                db.commit()
                db.refresh(user)
                raise INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION
            if not user.is_active:
                raise INACTIVE_USER_CUSTOM_HTTP_EXCEPTION
        user.try_login(True)
        db.commit()
        db.refresh(user)
        return user


    async def get_current_user(
        self,
        token: str = Depends(OAUTH2_SCHEME),
    ):
        db = self.get_session()
        payload = await self.authentication_provider.validate_token(token)
        sub: str = payload.get("sub")
        if sub is None:
            raise INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION
        user = (
            db.query(self.sqlalchemy_model)
            .filter(or_(self.sqlalchemy_model.username == sub, self.sqlalchemy_model.email == sub))
            .first()
        )
        if user is None:
            raise INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION
        return user


    async def refresh_token(self, refresh_token_data: RefreshToken):
        db = self.authentication_provider.get_session()
        payload = await self.authentication_provider.validate_token(refresh_token_data.refresh_token)
        sub = payload.get("sub")
        if sub is None:
            raise INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION
        user = (
            db.query(self.sqlalchemy_model)
            .filter(or_(self.sqlalchemy_model.username == sub, self.sqlalchemy_model.email == sub))
            .first()
        )
        if user is None:
            raise INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION
        access_token_expiration = timedelta(milliseconds=self.authentication_provider.access_token_expiration)
        access_token = self.create_access_token(
            data={"sub": sub}, expires_delta=access_token_expiration
        )
        return access_token
