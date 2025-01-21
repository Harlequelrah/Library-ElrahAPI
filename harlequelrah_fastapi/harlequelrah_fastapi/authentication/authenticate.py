from typing import List, Optional
from harlequelrah_fastapi.exception.auth_exception import (
    INACTIVE_USER_CUSTOM_HTTP_EXCEPTION,
    INSUFICIENT_PERMISSIONS_CUSTOM_HTTP_EXCEPTION,
    INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION,
)
from sqlalchemy.orm import Session, sessionmaker
from fastapi import Depends

from harlequelrah_fastapi.exception.exceptions_utils import raise_custom_http_exception
from .token import AccessToken, RefreshToken
from datetime import datetime, timedelta
from sqlalchemy import or_
import secrets
from fastapi.security import OAuth2PasswordBearer
from fastapi import status
from jose import ExpiredSignatureError, jwt, JWTError
from harlequelrah_fastapi.user.models import (
    UserPydanticModel,
    UserCreateModel,
    UserUpdateModel,
    UserModel as User,
)


class Authentication:
    TOKEN_URL = "users/tokenUrl"
    OAUTH2_SCHEME=OAuth2PasswordBearer(TOKEN_URL)
    UserPydanticModel = UserPydanticModel
    User = User
    UserCreateModel = UserCreateModel
    UserUpdateModel = UserUpdateModel
    ALGORITHMS = ["HS256"]
    REFRESH_TOKEN_EXPIRE_DAYS = 7
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def __init__(
        self,
        database_username: str,
        database_password: str,
        connector: str,
        database_name: str,
        server: str,
    ):
        self.database_username = database_username
        self.database_password = database_password
        self.connector = connector
        self.database_name = database_name
        self.server = server
        self.__secret_key = str(secrets.token_hex(32))
        self.__algorithm= self.ALGORITHMS[0]
        self.__session_factory:sessionmaker[Session]  = None

    @property
    def algorithm(self):
        return self.__algorithm

    @algorithm.setter
    def algorithms(self,algorithm:str):
        self.__algorithm=algorithm

    def set_oauth2_scheme(self,OAUTH2_CLASS:type):
        self.OAUTH2_SCHEME = OAUTH2_CLASS(self.TOKEN_URL)

    @property
    def session_factory(self):
        return self.__session_factory

    @session_factory.setter
    def session_factory(self, session_factory: sessionmaker[Session]):
        self.__session_factory = session_factory

    def get_session(self):
        db= self.__session_factory()
        if not db :  raise_custom_http_exception(status_code=status.HTTP_404_NOT_FOUND,detail="Session Factory Not Found")
        return db

    def check_authorization(self,privilege_name:Optional[List[str]]=None,roles_name:Optional[List[str]]=None)->callable:
        async def is_authorized(token:str=Depends(self.get_access_token))-> bool:
            payload= await self.validate_token(token)
            sub= payload.get('sub')
            db= self.get_session()
            user = await self.get_user_by_sub(username_or_email=sub,db=db)
            if not user : raise_custom_http_exception(status_code=status.HTTP_404_NOT_FOUND,detail="User Not Found")
            if roles_name:
                return user.has_role(roles_name)
            elif privilege_name:
                return user.has_privilege(privilege_name)
            else :raise INSUFICIENT_PERMISSIONS_CUSTOM_HTTP_EXCEPTION
        return is_authorized







    async def get_user_by_sub(self,username_or_email:str,db:Session):
        user = (
            db.query(self.User)
            .filter(
                or_(
                    self.User.username == username_or_email,
                    self.User.email == username_or_email,
                )
            )
            .first()
        )
        if user is None:
            raise INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION
        return user

    async def authenticate_user(
        self,
        password: str,
        username_or_email: Optional[str] = None,
        session: Optional[Session] = None,
    ):
        if username_or_email is None:
            raise INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION
        db = session if session else self.get_session()
        user = await self.get_user_by_sub(db=db,username_or_email=username_or_email)
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

    def create_access_token(
        self, data: dict, expires_delta: timedelta = None
    ) -> AccessToken:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(to_encode, self.__secret_key, algorithm=self.__algorithm)
        return {"access_token": encode_jwt, "token_type": "bearer"}

    def create_refresh_token(
        self, data: dict, expires_delta: timedelta = None
    ) -> RefreshToken:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=self.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(to_encode, self.__secret_key, algorithm=self.__algorithm)
        return {"refresh_token": encode_jwt, "token_type": "bearer"}

    async def get_access_token(self, token= Depends(OAUTH2_SCHEME)):
        await self.validate_token(token)
        return token

    async def get_current_user(
        self,
        token: str = Depends(OAUTH2_SCHEME),
    ):
        db = self.get_session()
        payload = await self.validate_token(token)
        sub: str = payload.get("sub")
        if sub is None:
            raise INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION
        user = (
            db.query(self.User)
            .filter(or_(self.User.username == sub, self.User.email == sub))
            .first()
        )
        if user is None:
            raise INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION
        return user

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

    async def refresh_token(self, refresh_token_data: RefreshToken):
        db = self.get_session()
        payload = await self.validate_token(refresh_token_data.refresh_token)
        sub = payload.get("sub")
        if sub is None:
            raise INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION
        user = (
            db.query(self.User)
            .filter(or_(self.User.username == sub, self.User.email == sub))
            .first()
        )
        if user is None:
            raise INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION
        ACCESS_TOKEN_EXPIRE_MINUTES = timedelta(self.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={"sub": sub}, expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        return access_token
