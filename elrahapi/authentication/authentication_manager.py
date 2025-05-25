from datetime import datetime, timedelta
from typing import Any, List, Optional
from elrahapi.utility.types import ElrahSession
from elrahapi.authentication.authentication_namespace import (
    ACCESS_TOKEN_EXPIRATION,
    OAUTH2_SCHEME,
    REFRESH_TOKEN_EXPIRATION,
)
from elrahapi.authentication.token import AccessToken, RefreshToken
from elrahapi.crud.crud_models import CrudModels
from elrahapi.exception.auth_exception import (
    INACTIVE_USER_CUSTOM_HTTP_EXCEPTION,
    INSUFICIENT_PERMISSIONS_CUSTOM_HTTP_EXCEPTION,
    INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION,
)
from elrahapi.exception.exceptions_utils import raise_custom_http_exception
from elrahapi.security.secret import define_algorithm_and_key
from elrahapi.utility.utils import exec_stmt, is_async_session
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy import or_, select
from fastapi import Depends, status


class AuthenticationManager:

    def __init__(
        self,
        secret_key: Optional[str] = None,
        algorithm: Optional[str] = None,
        refresh_token_expiration: Optional[int] = None,
        access_token_expiration: Optional[int] = None,
    ):
        self.__authentication_models: CrudModels = None
        self.__refresh_token_expiration = (
            refresh_token_expiration
            if refresh_token_expiration
            else REFRESH_TOKEN_EXPIRATION
        )
        self.__access_token_expiration = (
            access_token_expiration
            if access_token_expiration
            else ACCESS_TOKEN_EXPIRATION
        )
        self.__algorithm, self.__secret_key = define_algorithm_and_key(
            secret_key,
            algorithm,
        )

    @property
    def authentication_models(self):
        return self.__authentication_models

    @authentication_models.setter
    def authentication_models(self, authentication_models: CrudModels):
        self.__authentication_models = authentication_models

    @property
    def algorithm(self):
        return self.__algorithm

    @algorithm.setter
    def algorithms(self, algorithm: str):
        self.__algorithm = algorithm

    @property
    def access_token_expiration(self):
        return self.__access_token_expiration

    @access_token_expiration.setter
    def access_token_expiration(self, access_token_expiration: int):
        self.__access_token_expiration = access_token_expiration

    @property
    def refresh_token_expiration(self):
        return self.__refresh_token_expiration

    @refresh_token_expiration.setter
    def refresh_token_expiration(self, refresh_token_expiration: int):
        self.__refresh_token_expiration = refresh_token_expiration

    def create_access_token(
        self, data: dict, expires_delta: timedelta = None
    ) -> AccessToken:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(
                milliseconds=self.__access_token_expiration
            )
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(
            to_encode, self.__secret_key, algorithm=self.__algorithm
        )
        return {"access_token": encode_jwt, "token_type": "bearer"}

    def create_refresh_token(
        self, data: dict, expires_delta: timedelta = None
    ) -> RefreshToken:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(
                milliseconds=self.__refresh_token_expiration
            )
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(
            to_encode, self.__secret_key, algorithm=self.__algorithm
        )
        return {"refresh_token": encode_jwt, "token_type": "bearer"}

    def get_access_token(self, token=Depends(OAUTH2_SCHEME)):
        self.validate_token(token)
        return token

    def validate_token(self, token: str):
        try:
            payload = jwt.decode(token, self.__secret_key, algorithms=self.__algorithm)
            return payload
        except ExpiredSignatureError:
            raise_custom_http_exception(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
            )
        except JWTError:
            raise_custom_http_exception(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

    async def change_user_state(self, session: ElrahSession, pk: Any):
        pk_attr = self.__authentication_models.get_pk()
        stmt = select(self.__authentication_models.sqlalchemy_model).where(
            pk_attr == pk
        )
        result = await exec_stmt(stmt=stmt, session=session, with_scalars=False)
        user = result.scalar_one_or_none()
        if user:
            user.change_user_state()
            if is_async_session(session):
                await session.commit()
                await session.refresh(user)
            else:
                session.commit()
                session.refresh(user)
        else:
            detail = "User Not Found"
            raise_custom_http_exception(
                status_code=status.HTTP_404_NOT_FOUND, detail=detail
            )

    async def get_user_by_sub(self, sub: str,session: ElrahSession):
        stmt = select(self.__authentication_models.sqlalchemy_model).where(
            or_(
                self.__authentication_models.sqlalchemy_model.username
                == sub,
                self.__authentication_models.sqlalchemy_model.email
                == sub,
            )
        )
        result = await exec_stmt(
            stmt=stmt,
            session=session,
            with_scalars=False,
        )
        user = result.scalar_one_or_none()
        if user is None:
            raise INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION
        return user

    def check_authorization(
        self,
        session:ElrahSession,
        privilege_name: Optional[List[str]] = None,
        role_name: Optional[List[str]] = None,
    ) -> callable:
        async def is_authorized(
            token: str = Depends(self.get_access_token),
        ) -> bool:
            if role_name and privilege_name:
                raise_custom_http_exception(
                    status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "Cannot check role and privilege in the same time",
                )
            payload =  self.validate_token(token)
            sub = payload.get("sub")
            user = await self.get_user_by_sub(sub=sub,session=session)
            if not user:
                raise_custom_http_exception(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found"
                )
            if role_name:
                return user.has_role(role_name=role_name)
            elif privilege_name:
                return user.has_privilege(privilege_name)
            else:
                raise INSUFICIENT_PERMISSIONS_CUSTOM_HTTP_EXCEPTION

        return is_authorized

    def check_authorizations(
        self,
        session:ElrahSession,
        privileges_name: Optional[List[str]] = None,
        roles_name: Optional[List[str]] = None,
    ) -> List[callable]:
        authorizations = []
        for privilege_name in privileges_name:
            authorizations.append(
                self.check_authorization(session=session,privilege_name=privilege_name)
            )
        for role_name in roles_name:
            authorizations.append(self.check_authorization(session=session,role_name=role_name))
        return authorizations

    async def authenticate_user(
        self,
        password: str,
        session: ElrahSession,
        sub: Optional[str] = None,
    ):
        if sub is None:
            raise INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION
        user = await self.get_user_by_sub(session=session, sub=sub)
        if user:
            if not user.check_password(password):
                user.try_login(False)
                if is_async_session(session):
                    await session.commit()
                    await session.refresh(user)
                else:
                    session.commit()
                    session.refresh(user)
                raise INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION
            if not user.is_active:
                raise INACTIVE_USER_CUSTOM_HTTP_EXCEPTION
        user.try_login(True)
        if is_async_session(session):
            await session.commit()
            await session.refresh(user)
        else:
            session.commit()
            session.refresh(user)
        return user

    def get_current_user_sub(
        self,
        token: str = Depends(OAUTH2_SCHEME),
    ):
        payload =  self.validate_token(token)
        sub: str = payload.get("sub")
        if sub is None:
            raise INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION
        return sub

    async def refresh_token(
        self, session: ElrahSession, refresh_token_data: RefreshToken
    ):
        payload =  self.validate_token(refresh_token_data.refresh_token)
        sub = payload.get("sub")
        if sub is None:
            raise INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION
        stmt = select(self.__authentication_models.sqlalchemy_model).where(
            or_(
                self.__authentication_models.sqlalchemy_model.username == sub,
                self.__authentication_models.sqlalchemy_model.email == sub,
            )
        )
        result = await exec_stmt(
            stmt=stmt,
            session=session,
            with_scalars=False,
        )
        user = result.scalar_one_or_none()
        if user is None:
            raise INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION
        access_token_expiration = timedelta(milliseconds=self.__access_token_expiration)
        access_token = self.create_access_token(
            data={"sub": sub}, expires_delta=access_token_expiration
        )
        return access_token

    async def is_existing_user(self,session:ElrahSession, sub: str):
        user= await self.get_user_by_sub(sub=sub,session=session)
        return user is not None

    async def read_one_user(self,session:ElrahSession,sub: str):
        user= await self.get_user_by_sub(sub=sub,session=session)
        if not user:
            detail = f"User with username or email {sub} not found"
            raise_custom_http_exception(
                status_code=status.HTTP_404_NOT_FOUND, detail=detail
            )
        return user

    async def change_password(
        self,session:ElrahSession, sub: str, current_password: str, new_password: str
    ):
        current_user = await self.authenticate_user(
            password=current_password,
            sub=sub,
            session=session,
        )
        current_user.password = new_password
        if is_async_session(session):
            await session.commit()
            await session.refresh(current_user)
        else:
            session.commit()
            session.refresh(current_user)
