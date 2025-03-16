
from sqlalchemy.orm import Session, sessionmaker
from elrahapi.authentication.authentication_namespace import ACCESS_TOKEN_EXPIRATION, OAUTH2_SCHEME, REFRESH_TOKEN_EXPIRATION
from elrahapi.crud.crud_models import CrudModels
from elrahapi.security.secret import define_algorithm_and_key
from elrahapi.authentication.token import AccessToken, RefreshToken
from datetime import datetime, timedelta
from jose import ExpiredSignatureError, jwt, JWTError
from typing import List, Optional
from fastapi import Depends,status
from sqlalchemy import or_
from elrahapi.exception.auth_exception import INACTIVE_USER_CUSTOM_HTTP_EXCEPTION, INSUFICIENT_PERMISSIONS_CUSTOM_HTTP_EXCEPTION, INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION
from elrahapi.exception.exceptions_utils import raise_custom_http_exception

class AuthenticationManager:

    def __init__(
        self,
        database_username: str,
        database_password: str,
        connector: str,
        database_name: str,
        server: str,
        secret_key: Optional[str] = None,
        algorithm: Optional[str] = None,
        refresh_token_expiration: Optional[int] = None,
        access_token_expiration: Optional[int] = None,
    ):
        self.__database_username = database_username
        self.__database_password = database_password
        self.__connector = connector
        self.__database_name = database_name
        self.__server = server
        self.__authentication_models:CrudModels
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
        self.__session_factory: sessionmaker[Session] = None

    @property
    def authentication_models(self):
        return self.__authentication_models

    @authentication_models.setter
    def authentication_models(self,authentication_models:CrudModels):
        self.__authentication_models = authentication_models

    @property
    def database_username(self):
        return self.__database_username

    @database_username.setter
    def database_username(self, database_username: str):
        self.__database_username = database_username

    @property
    def database_password(self):
        return self.__database_password

    @database_password.setter
    def database_password(self, database_password: str):
        self.__database_password = database_password

    @property
    def connector(self):
        return self.__connector

    @connector.setter
    def connector(self, connector: str):
        self.__connector = connector

    @property
    def database_name(self):
        return self.__database_name

    @database_name.setter
    def database_name(self, database_name: str):
        self.__database_name = database_name

    @property
    def server(self):
        return self.__server

    @server.setter
    def server(self, server: str):
        self.__server = server

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


    @property
    def session_factory(self):
        return self.__session_factory

    @session_factory.setter
    def session_factory(self, session_factory: sessionmaker[Session]):
        self.__session_factory = session_factory

    def get_session(self):
        db = self.__session_factory()
        if not db:
            raise_custom_http_exception(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session Factory Not Found",
            )
        return db

    def create_access_token(
        self, data: dict, expires_delta: timedelta = None
    ) -> AccessToken:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
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
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
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

    async def get_user_by_sub(self, username_or_email: str, db: Session):
        user = (
            db.query(self.__authentication_models.sqlalchemy_model)
            .filter(
                or_(
                    self.__authentication_models.sqlalchemy_model.username == username_or_email,
                    self.__authentication_models.sqlalchemy_model.email == username_or_email,
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
        async def is_authorized(token: str = Depends(self.get_access_token)) -> bool:
            payload = await self.validate_token(token)
            sub = payload.get("sub")
            db = self.get_session()
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
        db = session if session else self.get_session()
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
        payload = await self.validate_token(token)
        sub: str = payload.get("sub")
        if sub is None:
            raise INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION
        user =(
                db.query(self.__authentication_models.sqlalchemy_model)
                .filter(or_(
                    self.__authentication_models.sqlalchemy_model.username == sub, self.__authentication_models.sqlalchemy_model.email == sub))
                .first()
            )
        if user is None:
            raise INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION
        return user


    async def refresh_token(self, refresh_token_data: RefreshToken):
        db = self.get_session()
        payload = await self.validate_token(refresh_token_data.refresh_token)
        sub = payload.get("sub")
        if sub is None:
            raise INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION
        user =(
            db.query(self.__authentication_models.sqlalchemy_model)
            .filter(or_(self.__authentication_models.sqlalchemy_model.username == sub, self.__authentication_models.sqlalchemy_model.email == sub))
            .first()
            )
        if user is None:
            raise INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION
        access_token_expiration = timedelta(milliseconds=self.__access_token_expiration)
        access_token = self.create_access_token(
            data={"sub": sub}, expires_delta=access_token_expiration
        )
        return access_token

    async def is_unique(self, sub: str):
        db = self.get_session()
        user =(
                db.query(self.__authentication_models.sqlalchemy_model.sqlalchemy_model)
                .filter(
                    or_(
                        self.__authentication_models.sqlalchemy_model.sqlalchemy_model.email == sub,
                        self.__authentication_models.sqlalchemy_model.sqlalchemy_model.username == sub,
                    )
                )
                .first()
        )
        return user is None

    async def read_one_user(self, username_or_email: str):
        session = self.session_factory()
        user =(
                session.query(self.__authentication_models.sqlalchemy_model)
                .filter(
                    or_(
                        self.__authentication_models.sqlalchemy_model.username == username_or_email,
                        self.__authentication_models.sqlalchemy_model.email == username_or_email,
                    )
                )
                .first()
        )
        if not user:
            detail = f"User with username or email {username_or_email} not found"
            raise_custom_http_exception(
                status_code=status.HTTP_404_NOT_FOUND, detail=detail
            )
        return user

    async def change_password(
        self, username_or_email: str, current_password: str, new_password: str
    ):
        session = self.session_factory()
        current_user = await self.authenticate_user(
            password=current_password,
            username_or_email=username_or_email,
            session=session,
        )
        if current_user.check_password(current_password):
            current_user.set_password(new_password)
            session.commit()
            session.refresh(current_user)
        else:
            raise_custom_http_exception(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Your current password you enter  is incorrect",
            )

