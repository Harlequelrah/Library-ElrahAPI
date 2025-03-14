from typing import Optional
from sqlalchemy.orm import Session, sessionmaker
from fastapi import Depends
from elrahapi.authentication.authentication_namespace import ACCESS_TOKEN_EXPIRATION, OAUTH2_SCHEME, REFRESH_TOKEN_EXPIRATION
from elrahapi.exception.exceptions_utils import raise_custom_http_exception
from elrahapi.security.secret import define_algorithm_and_key
from .token import AccessToken, RefreshToken
from datetime import datetime, timedelta
from fastapi import status
from jose import ExpiredSignatureError, jwt, JWTError



class AuthenticationProvider:

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


