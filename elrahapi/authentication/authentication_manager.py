import os
from datetime import datetime, timedelta
from typing import Any

from dotenv import load_dotenv
from elrahapi.authentication.authentication_namespace import (
    ACCESS_TOKEN_EXPIRATION,
    REFRESH_TOKEN_EXPIRATION,
    TEMP_TOKEN_EXPIRATION,
    TOKEN_URL,
)
from elrahapi.authentication.token import (
    AccessToken,
    RefreshToken,
    TempToken,
    Token,
    TokenType,
)
from elrahapi.crud.crud_models import CrudModels
from elrahapi.database.session_manager import SessionManager
from elrahapi.exception.auth_exception import (
    INACTIVE_USER_CUSTOM_HTTP_EXCEPTION,
    INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION,
)
from elrahapi.exception.custom_http_exception import CustomHttpException
from elrahapi.exception.exceptions_utils import raise_custom_http_exception
from elrahapi.security.secret import define_algorithm_and_key
from elrahapi.utility.types import ElrahSession
from elrahapi.utility.utils import exec_stmt
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
)
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy import select
from sqlalchemy.sql import or_

from fastapi import Depends, status

load_dotenv(".env")

ISSUER = os.getenv("ISSUER")
AUDIENCE = os.getenv("AUDIENCE")


class AuthenticationManager:

    def __init__(
        self,
        authentication_models: CrudModels,
        session_manager: SessionManager,
        secret_key: str | None = None,
        algorithm: str | None = None,
        refresh_token_expiration: int | None = None,
        access_token_expiration: int | None = None,
        temp_token_expiration: int | None = None,
        security: OAuth2PasswordBearer | HTTPBearer | None = None,
    ):
        self.__authentication_models: CrudModels = authentication_models
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
        self.__temp_token_expiration = (
            temp_token_expiration if temp_token_expiration else TEMP_TOKEN_EXPIRATION
        )
        self.__algorithm, self.__secret_key = define_algorithm_and_key(
            secret_key,
            algorithm,
        )
        self.__session_manager: SessionManager = session_manager
        self.security = (
            security if security else OAuth2PasswordBearer(tokenUrl=TOKEN_URL)
        )

        def get_oauth2passwordbearer_token(token: str = Depends(self.security)):
            self.validate_token(token)
            return token

        def get_httpbearer_token(
            credentials: HTTPAuthorizationCredentials = Depends(self.security),
        ):
            token = credentials.credentials
            self.validate_token(token=token)
            return token

        self.get_access_token: callable = (
            get_oauth2passwordbearer_token
            if isinstance(self.security, OAuth2PasswordBearer)
            else get_httpbearer_token
        )

        def get_current_user_sub(token: str = Depends(self.get_access_token)):
            payload = self.validate_token(token)
            sub: str = payload.get("sub")
            if sub is None:
                raise INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION
            return sub

        self.get_current_user_sub = get_current_user_sub

    @property
    def session_manager(self) -> SessionManager:
        return self.__session_manager

    @session_manager.setter
    def session_manager(self, session_manager: SessionManager):
        self.__session_manager = session_manager

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

    def get_token_duration(self, token_type: TokenType) -> int:
        if token_type == TokenType.ACCESS_TOKEN:
            duration = self.__access_token_expiration
        elif token_type == TokenType.REFRESH_TOKEN:
            duration = self.__refresh_token_expiration
        else:
            duration = self.__temp_token_expiration
        return int(duration)

    def create_token(
        self, data: dict, token_type: TokenType, expires_delta: timedelta = None
    ) -> AccessToken | RefreshToken | TempToken:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            milliseconds: int = self.get_token_duration(token_type=token_type)
            expire = datetime.now() + timedelta(milliseconds=milliseconds)
        iat = datetime.now()
        to_encode.update({"exp": expire, "iat": iat})
        if ISSUER:
            to_encode.update({"iss": ISSUER})
        if AUDIENCE:
            to_encode.update({"aud": AUDIENCE})
        encode_jwt = jwt.encode(
            to_encode, self.__secret_key, algorithm=self.__algorithm
        )
        return {token_type.value: encode_jwt, "token_type": "bearer"}

    def validate_token(self, token: str):
        try:
            payload = jwt.decode(token, self.__secret_key, algorithms=self.__algorithm)
            return payload
        except ExpiredSignatureError as experr:
            raise_custom_http_exception(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token has expired : {str(experr)}",
            )
        except JWTError as jwterr:
            raise_custom_http_exception(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token : {str(jwterr)}",
            )
        except Exception as err:
            raise_custom_http_exception(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error decoding token :  {str(err)}",
            )

    async def change_user_state(self, pk: Any, session: ElrahSession):
        try:
            pk_attr = self.__authentication_models.get_pk()
            stmt = select(self.__authentication_models.sqlalchemy_model).where(
                pk_attr == pk
            )
            result = await exec_stmt(stmt=stmt, session=session)
            user = result.scalar_one_or_none()
            if user:
                user.change_user_state()
                await self.session_manager.commit_and_refresh(
                    session=session, object=user
                )
            else:
                detail = "User Not Found"
                raise_custom_http_exception(
                    status_code=status.HTTP_404_NOT_FOUND, detail=detail
                )
        except CustomHttpException as che:
            await self.session_manager.rollback_session(session=session)
            raise che
        except Exception as e:
            await self.session_manager.rollback_session(session=session)
            detail = f"Error while changing user state: {str(e)}"
            raise_custom_http_exception(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
            )

    async def get_user_by_sub(self, sub: str | int, session: ElrahSession):
        try:
            pk_attr = self.__authentication_models.get_pk()
            email_attr = self.__authentication_models.sqlalchemy_model.email
            username_attr = self.__authentication_models.sqlalchemy_model.username
            if isinstance(sub, str) and sub.isdigit():
                sub = int(sub)
            if isinstance(sub, int):
                stmt = select(self.__authentication_models.sqlalchemy_model).where(
                    pk_attr == sub
                )
            else:
                stmt = select(self.__authentication_models.sqlalchemy_model).where(
                    or_(email_attr == sub, username_attr == sub)
                )
            result = await exec_stmt(stmt=stmt, session=session)
            user = result.scalar_one_or_none()
            if user is None:
                raise INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION
            return user
        except CustomHttpException as che:
            await self.session_manager.rollback_session(session=session)
            raise che
        except Exception as e:
            await self.session_manager.rollback_session(session=session)
            detail = f"Error while getting user by sub: {str(e)}"
            raise_custom_http_exception(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
            )

    async def is_authorized(
        self,
        sub: str,
        privilege_name: str | None = None,
        role_name: str | None = None,
    ) -> bool:
        try:
            session: ElrahSession = await self.session_manager.get_session()
            user = await self.get_user_by_sub(sub=sub, session=session)
            if role_name:
                return user.has_role(role_name=role_name)
            elif privilege_name:
                return user.has_privilege(privilege_name)
        except CustomHttpException as che:
            await self.session_manager.rollback_session(session=session)
            raise che
        except Exception as e:
            await self.session_manager.rollback_session(session=session)
            detail = "Error while checking authorization: " + str(e)
            raise_custom_http_exception(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
            )
        finally:
            await self.session_manager.close_session(session=session)

    def get_sub_from_token(self, token: str) -> str | int:
        payload = self.validate_token(token)
        sub: str = payload.get("sub")
        if sub.isdigit():
            sub = int(sub)
        return sub

    def check_authorization(
        self,
        privilege_name: str | None = None,
        role_name: str | None = None,
    ) -> callable:
        async def auth_result(
            token: str = Depends(self.get_access_token),
        ):
            sub = self.get_sub_from_token(token=token)
            if role_name and sub:
                return await self.is_authorized(
                    sub=sub,
                    role_name=role_name,
                )
            elif privilege_name and sub:
                return await self.is_authorized(
                    sub=sub,
                    privilege_name=privilege_name,
                )
            elif (role_name and privilege_name) or (
                not role_name and not privilege_name
            ):
                raise_custom_http_exception(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Either role or privilege must be provided, not both or any",
                )
            else:
                raise_custom_http_exception(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Sub must be provided , Maybe User is not authenticated",
                )

        return auth_result

    def check_authorizations(
        self,
        privileges_name: list[str] | None = None,
        roles_name: list[str] | None = None,
    ) -> list[callable]:
        authorizations = []
        for privilege_name in privileges_name:
            authorizations.append(
                self.check_authorization(privilege_name=privilege_name)
            )
        for role_name in roles_name:
            authorizations.append(self.check_authorization(role_name=role_name))
        return authorizations

    def build_login_token(
        self, access_token_data: str, refresh_token_data: str
    ) -> Token:
        access_token_data = self.create_token(
            data=access_token_data, token_type=TokenType.ACCESS_TOKEN
        )
        refresh_token_data = self.create_token(
            data=refresh_token_data, token_type=TokenType.REFRESH_TOKEN
        )
        return {
            TokenType.ACCESS_TOKEN.value: access_token_data.get(
                TokenType.ACCESS_TOKEN.value
            ),
            TokenType.REFRESH_TOKEN.value: refresh_token_data.get(
                TokenType.REFRESH_TOKEN.value
            ),
            "token_type": "bearer",
        }

    async def authenticate_user(
        self,
        password: str,
        session: ElrahSession,
        sub: str | None = None,
    ):
        try:
            if sub is None:
                raise INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION
            user = await self.get_user_by_sub(session=session, sub=sub)
            if user:
                if not user.check_password(password):
                    user.try_login(False)
                    await self.session_manager.commit_and_refresh(
                        session=session, object=user
                    )
                    raise INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION
                if not user.is_active:
                    raise INACTIVE_USER_CUSTOM_HTTP_EXCEPTION
            user.try_login(True)
            await self.session_manager.commit_and_refresh(session=session, object=user)
            return user
        except CustomHttpException as che:
            await self.session_manager.rollback_session(session=session)
            raise che
        except Exception as e:
            await self.session_manager.rollback_session(session=session)
            detail = f"Error while authenticating user: {str(e)}"
            raise_custom_http_exception(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
            )

    async def refresh_token(
        self, session: ElrahSession, refresh_token_data: RefreshToken
    ):
        try:
            sub = self.get_sub_from_token(token=refresh_token_data.refresh_token)
            if sub is None:
                raise INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION
            user = await self.get_user_by_sub(sub=sub, session=session)
            access_token_expiration = timedelta(
                milliseconds=self.__access_token_expiration
            )
            data = user.build_access_token_data(authentication=self)
            access_token = self.create_token(
                data=data,
                expires_delta=access_token_expiration,
                token_type=TokenType.ACCESS_TOKEN,
            )
            return access_token
        except CustomHttpException as che:
            await self.session_manager.rollback_session(session=session)
            raise che
        except Exception as e:
            await self.session_manager.rollback_session(session=session)
            detail = f"Error while refreshing token: {str(e)}"
            raise_custom_http_exception(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
            )

    async def is_existing_user(self, session: ElrahSession, sub: str):
        user = await self.get_user_by_sub(sub=sub, session=session)
        return user is not None

    async def read_one_user(self, session: ElrahSession, sub: str):
        try:
            user = await self.get_user_by_sub(sub=sub, session=session)
            return user
        except CustomHttpException as che:
            await self.session_manager.rollback_session(session=session)
            raise che
        except Exception as e:
            await self.session_manager.rollback_session(session=session)
            detail = f"Error while reading user with sub {sub} , details : {str(e)}"
            raise_custom_http_exception(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
            )

    async def change_password(
        self, session: ElrahSession, sub: str, current_password: str, new_password: str
    ):
        current_user = await self.authenticate_user(
            password=current_password,
            sub=sub,
            session=session,
        )
        current_user.password = new_password
        await self.session_manager.commit_and_refresh(
            session=session, object=current_user
        )
