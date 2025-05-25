from datetime import datetime, timedelta
from typing import List, Optional

from elrahapi.authentication.authentication_namespace import (
    ACCESS_TOKEN_EXPIRATION,
    OAUTH2_SCHEME,
    REFRESH_TOKEN_EXPIRATION,
)
from elrahapi.authentication.token import AccessToken, RefreshToken
from elrahapi.crud.crud_models import CrudModels
from elrahapi.database.session_manager import SessionManager
from elrahapi.exception.auth_exception import (
    INACTIVE_USER_CUSTOM_HTTP_EXCEPTION,
    INSUFICIENT_PERMISSIONS_CUSTOM_HTTP_EXCEPTION,
    INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION,
)
from elrahapi.exception.exceptions_utils import raise_custom_http_exception
from elrahapi.security.secret import define_algorithm_and_key
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from fastapi import Depends, status

from elrahapi.utility.utils import exec_stmt


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
        self.__session_manager: SessionManager = None

    @property
    def session_manager(self) -> SessionManager:
        return self.__session_manager

    @session_manager.setter
    def session_manager(self, session_manager: SessionManager) -> None:
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

    async def get_session(self):
        if not self.__session_manager:
            raise_custom_http_exception(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Session manager is not set",
            )
        return await self.__session_manager.yield_session()

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

    async def get_access_token(self, token=Depends(OAUTH2_SCHEME)):
        await self.validate_token(token)
        return token

    async def validate_token(self, token: str):
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

    async def change_user_state(self,pk):
        db=  await self.get_session()
        pk_attr =  self.__authentication_models.get_pk()
        stmt = select(self.__authentication_models.sqlalchemy_model).where(
            pk_attr == pk
        )
        result = await exec_stmt(
            stmt=stmt,
            session=db,
            is_async_env=self.__session_manager.is_async_env,
            with_scalars=False
        )
        user=result.scalar_one_or_none()
        if user :
            user.change_user_state()
            db.commit()
            db.refresh(user)

        else :
            detail = "User Not Found"
            raise_custom_http_exception(
                status_code=status.HTTP_404_NOT_FOUND, detail=detail
            )

    async def get_user_by_sub(self, username_or_email: str, db: Session):
        stmt = select(self.__authentication_models.sqlalchemy_model).where(
            or_(
                self.__authentication_models.sqlalchemy_model.username
                == username_or_email,
                self.__authentication_models.sqlalchemy_model.email
                == username_or_email,
            )
        )
        result=await exec_stmt(
                stmt=stmt,
                session=db,
                is_async_env=self.__session_manager.is_async_env,
                with_scalars=False,
            )
        user = result.scalar_one_or_none()
        if user is None:
            raise INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION
        return user

    def check_authorization(
        self,
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
            payload = await self.validate_token(token)
            sub = payload.get("sub")
            db = await self.get_session()
            user = await self.get_user_by_sub(username_or_email=sub, db=db)
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
        privileges_name: Optional[List[str]] = None,
        roles_name: Optional[List[str]] = None,
    ) -> List[callable]:
        authorizations = []
        for privilege_name in privileges_name:
            authorizations.append(self.check_authorization(privilege_name=privilege_name))
        for role_name in roles_name:
            authorizations.append(self.check_authorization(role_name=role_name))
        return authorizations

    async def authenticate_user(
        self,
        password: str,
        username_or_email: Optional[str] = None,
        session: Optional[Session] = None,
    ):
        if username_or_email is None:
            raise INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION
        db = session if session else await self.get_session()
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
        db = await self.get_session()
        payload = await self.validate_token(token)
        sub: str = payload.get("sub")
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
            session=db,
            is_async_env=self.__session_manager.is_async_env,
            with_scalars=False,
        )
        user = result.scalar_one_or_none()
        if user is None:
            raise INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION
        return user

    async def refresh_token(self, refresh_token_data: RefreshToken):
        db = await self.get_session()
        payload = await self.validate_token(refresh_token_data.refresh_token)
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
            session=db,
            is_async_env=self.__session_manager.is_async_env,
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

    async def is_unique(self, sub: str):
        db = await self.get_session()
        stmt = select(
            self.__authentication_models.sqlalchemy_model.sqlalchemy_model
        ).where(
            or_(
                self.__authentication_models.sqlalchemy_model.sqlalchemy_model.email
                == sub,
                self.__authentication_models.sqlalchemy_model.sqlalchemy_model.username
                == sub,
            )
        )
        result = await exec_stmt(
            stmt=stmt,
            session=db,
            is_async_env=self.__session_manager.is_async_env,
            with_scalars=False,
        )
        user = result.scalar_one_or_none()
        return user is None

    async def read_one_user(self, username_or_email: str):
        session = await self.session_manager.yield_session()
        stmt = select(self.__authentication_models.sqlalchemy_model).where(
            or_(
                self.__authentication_models.sqlalchemy_model.username
                == username_or_email,
                self.__authentication_models.sqlalchemy_model.email
                == username_or_email,
            )
        )
        result = await exec_stmt(
            stmt=stmt,
            session=session,
            is_async_env=self.__session_manager.is_async_env,
            with_scalars=False,
        )
        user = result.scalar_one_or_none()
        if not user:
            detail = f"User with username or email {username_or_email} not found"
            raise_custom_http_exception(
                status_code=status.HTTP_404_NOT_FOUND, detail=detail
            )
        return user

    async def change_password(
        self, username_or_email: str, current_password: str, new_password: str
    ):
        session = await self.session_manager.yield_session()
        current_user = await self.authenticate_user(
            password=current_password,
            username_or_email=username_or_email,
            session=session,
        )
        if current_user.check_password(current_password):
            current_user.password = new_password
            session.commit()
            session.refresh(current_user)
        else:
            raise_custom_http_exception(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Your current password you enter  is incorrect",
            )
