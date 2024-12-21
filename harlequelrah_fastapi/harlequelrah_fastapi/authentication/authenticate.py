from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session,sessionmaker

from harlequelrah_fastapi.exception.custom_http_exception import CustomHttpException
from .token import AccessToken,RefreshToken
from datetime import datetime, timedelta
from sqlalchemy import or_
import secrets
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from harlequelrah_fastapi.user.models import UserPydanticModel,UserCreateModel,UserLoginModel,UserUpdateModel,User
HTTP_EXCEPTION=HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
AUTHENTICATION_EXCEPTION = CustomHttpException(HTTP_EXCEPTION)
class Authentication():
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/tokenUrl")
    UserPydanticModel=UserPydanticModel
    User=User
    UserCreateModel=UserCreateModel
    UserUpdateModel=UserUpdateModel
    UserLoginModel=UserLoginModel
    SECRET_KEY = str(secrets.token_hex(32))
    ALGORITHM = "HS256"
    REFRESH_TOKEN_EXPIRE_DAYS = 7
    ACCESS_TOKEN_EXPIRE_MINUTES= 30
    session_factory:sessionmaker[Session]=None
    CREDENTIALS_EXCEPTION = AUTHENTICATION_EXCEPTION
    def __init__(self,database_username:str,database_password:str,connector:str,database_name:str,server:str):
        self.database_username=database_username
        self.database_password=database_password
        self.connector=connector
        self.database_name=database_name
        self.server=server

    def set_db_session(self,session_factory):
        self.session_factory=session_factory
    def get_session(self):
        return self.session_factory()

    def set_algorithm(self,algorithm):
        self.ALGORITHM=algorithm

    def set_REFRESH_TOKEN_EXPIRE_DAYS(self,REFRESH_TOKEN_EXPIRE_DAYS):
        self.REFRESH_TOKEN_EXPIRE_DAYS=REFRESH_TOKEN_EXPIRE_DAYS

    def set_ACCESS_TOKEN_EXPIRE_MINUTES(self,ACCESS_TOKEN_EXPIRE_MINUTES):
        self.ACCESS_TOKEN_EXPIRE_MINUTES=ACCESS_TOKEN_EXPIRE_MINUTES

    def set_authentication_scheme(self,oauth2_scheme):
        self.oauth2_scheme=oauth2_scheme

    async def authenticate_user(self, username_or_email: str, password: str):
        db=self.get_session()
        user = (
        db.query(self.User)
        .filter(or_(self.User.username == username_or_email ,self.User.email == username_or_email))
        .first()
    )
        if user and not user.check_password(password):
            user.try_login(False)
        if not user or not user.check_password(password) or not user.is_active:
            raise self.self.CREDENTIALS_EXCEPTION
        user.try_login(True)
        db.commit()
        db.refresh(user)
        return user

    def create_access_token(self,data:dict, expires_delta: timedelta = None) -> AccessToken:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return {"access_token":encode_jwt,"token_type":"bearer"}

    def create_refresh_token(self,data: dict, expires_delta: timedelta = None) -> RefreshToken:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=self.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return {"refresh_token":encode_jwt,"token_type":"bearer"}

    async def get_current_user(
        self, token: str = Depends(oauth2_scheme)
    ):
        try:
            db=self.get_session()
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            sub: str = payload.get("sub")
            if sub is None:
                raise self.CREDENTIALS_EXCEPTION
        except JWTError:
            raise self.CREDENTIALS_EXCEPTION
        user = db.query(self.User).filter(or_(self.User.username == sub,self.User.email == sub)).first()
        if user is None:
            print("user is none")
            raise self.CREDENTIALS_EXCEPTION
        return user

    def refresh_token(self,token:RefreshToken):
        try:
            db=self.self.get_session()
            payload=jwt.decode(token.refresh_token,self.SECRET_KEY,algorithms=[self.ALGORITHM])
            sub=payload.get("sub")
            if sub is None : raise self.CREDENTIALS_EXCEPTION
            user=db.query(self.User).filter(or_(self.User.username==sub , self.User.email==sub)).first()
            if user is None: raise self.CREDENTIALS_EXCEPTION
            ACCESS_TOKEN_EXPIRE_MINUTES=timedelta(self.ACCESS_TOKEN_EXPIRE_MINUTES_MINUTES)
            access_token=self.create_access_token(
                data={"sub":sub},expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES
            )
            return access_token
        except JWTError:
            raise self.CREDENTIALS_EXCEPTION
