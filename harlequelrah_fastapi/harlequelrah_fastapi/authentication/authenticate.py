from typing import Optional
from harlequelrah_fastapi.exception.auth_exception import (
    INACTIVE_USER_CUSTOM_HTTP_EXCEPTION,
    INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION,
)
from sqlalchemy.orm import Session, sessionmaker
from fastapi import Depends
from .token import AccessToken, RefreshToken
from datetime import datetime, timedelta
from sqlalchemy import or_
import secrets
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException as HE, status
from harlequelrah_fastapi.exception.custom_http_exception import (
    CustomHttpException as CHE,
)
from jose import ExpiredSignatureError, jwt, JWTError
from harlequelrah_fastapi.user.models import (
    UserPydanticModel,
    UserCreateModel,
    UserUpdateModel,
    User,
)


class Authentication:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/tokenUrl")
    UserPydanticModel = UserPydanticModel
    User = User
    UserCreateModel = UserCreateModel
    UserUpdateModel = UserUpdateModel
    SECRET_KEY = str(secrets.token_hex(32))
    ALGORITHM = "HS256"
    REFRESH_TOKEN_EXPIRE_DAYS = 7
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    session_factory: sessionmaker[Session] = None

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

    def set_db_session(self, session_factory):
        self.session_factory = session_factory

    def get_session(self):
        db = self.session_factory()
        return db

    def set_algorithm(self, algorithm):
        self.ALGORITHM = algorithm

    def set_REFRESH_TOKEN_EXPIRE_DAYS(self, REFRESH_TOKEN_EXPIRE_DAYS):
        self.REFRESH_TOKEN_EXPIRE_DAYS = REFRESH_TOKEN_EXPIRE_DAYS

    def set_ACCESS_TOKEN_EXPIRE_MINUTES(self, ACCESS_TOKEN_EXPIRE_MINUTES):
        self.ACCESS_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES

    def set_authentication_scheme(self, oauth2_scheme):
        self.oauth2_scheme = oauth2_scheme

    async def authenticate_user(
        self,
        password: str,
        username_or_email: Optional[str] = None,
        session: Optional[Session] = None,
    ):
        if username_or_email is None:
            raise INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION
        db = self.get_session() if session is None else session
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
        if user:
            if not user.check_password(password):
                user.try_login(False)
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
        encode_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
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
        encode_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return {"refresh_token": encode_jwt, "token_type": "bearer"}

    async def get_access_token(self, token=Depends(oauth2_scheme)):
        await self.validate_token(token)
        return token

    async def get_current_user(
        self,
        # token:str
        token: str = Depends(oauth2_scheme),
    ):
        db = self.get_session()
        payload = await self.validate_token(token)
        sub: str = payload.get("sub")
        if sub is None:
            raise self.CREDENTIALS_EXCEPTION
        user = (
            db.query(self.User)
            .filter(or_(self.User.username == sub, self.User.email == sub))
            .first()
        )
        if user is None:
            raise self.CREDENTIALS_EXCEPTION
        return user

    async def validate_token(self, token: str):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload
        except ExpiredSignatureError:
            detail = "Token has expired"
            http_exc = HE(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
            custom_http_exc = CHE(http_exc)
            raise custom_http_exc
        except JWTError:
            detail = "Invalid token"
            http_exc = HE(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
            custom_http_exc = CHE(http_exc)
            raise custom_http_exc

    async def refresh_token(self, refresh_token_data: RefreshToken):
        db = self.get_session()
        payload = await self.validate_token(refresh_token_data.refresh_token)
        sub = payload.get("sub")
        if sub is None:
            raise self.CREDENTIALS_EXCEPTION
        user = (
            db.query(self.User)
            .filter(or_(self.User.username == sub, self.User.email == sub))
            .first()
        )
        if user is None:
            raise self.CREDENTIALS_EXCEPTION
        ACCESS_TOKEN_EXPIRE_MINUTES = timedelta(self.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={"sub": sub}, expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        return access_token
