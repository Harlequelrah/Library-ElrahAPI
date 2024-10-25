from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from .token import AccessToken,RefreshToken
from datetime import datetime, timedelta
from sqlalchemy import or_
import secrets
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from harlequelrah_fastapi.user.models import UserModel,UserCreateModel,UserLoginModel,UserUpdateModel,User



class Authentication():
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="tokenUrl")
    UserModel=UserModel
    User=User
    UserCreateModel=UserCreateModel
    UserUpdateModel=UserUpdateModel
    UserLoginModel=UserLoginModel
    SECRET_KEY = str(secrets.token_hex(32))
    ALGORITHM = "HS256"
    REFRESH_TOKEN_EXPIRE_DAYS = 7
    ACCESS_TOKEN_EXPIRE_MINUTES= 30
    CREDENTIALS_EXCEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    def __init__(self,database_username,database_password):
        self.database_username=database_username
        self.database_password=database_password

    def set_algorithm(self,algorithm):
        self.ALGORITHM=algorithm
        return self.ALGORITHM

    def set_REFRESH_TOKEN_EXPIRE_DAYS(self,REFRESH_TOKEN_EXPIRE_DAYS):
        self.REFRESH_TOKEN_EXPIRE_DAYS=REFRESH_TOKEN_EXPIRE_DAYS
        return self.REFRESH_TOKEN_EXPIRE_DAYS

    def set_ACCESS_TOKEN_EXPIRE_MINUTES(self,ACCESS_TOKEN_EXPIRE_MINUTES):
        self.ACCESS_TOKEN_EXPIRE_MINUTES=ACCESS_TOKEN_EXPIRE_MINUTES
        return self.ACCESS_TOKEN_EXPIRE_MINUTES

    def set_authentication_scheme(self,oauth2_scheme):
        self.oauth2_scheme=oauth2_scheme
        return self.oauth2_scheme

    async def authenticate_user(self,db: Session, username_or_email: str, password: str):
        user = (
        db.query(self.User)
        .filter(or_(self.User.username == username_or_email ,self.User.email == username_or_email))
        .first()
    )
        if not user or not user.check_password(password) or not user.is_active:
            raise self.self.CREDENTIALS_EXCEPTION
        return user


    def create_access_token(self,data:dict, expires_delta: timedelta = None) -> AccessToken:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return {"access_token": encode_jwt, "token_type": "bearer"}


    def create_refresh_token(self,data: dict, expires_delta: timedelta = None) -> RefreshToken:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=self.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return {"refresh_token": encode_jwt,"token_type":"bearer"}


    async def get_current_user(self,db: Session,
        token: str = Depends(oauth2_scheme)
    ):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            sub: str = payload.get("sub")
            print("sub"+sub)
            if sub is None:
                print("sub is none")
                raise self.CREDENTIALS_EXCEPTION
        except JWTError:
            print("error decoding")
            raise self.CREDENTIALS_EXCEPTION
        user = db.query(self.User).filter(or_(self.User.username == sub,self.User.email == sub)).first()
        if user is None:
            print("user is none")
            raise self.CREDENTIALS_EXCEPTION
        return user


    def refresh_token(self,db:Session,token:RefreshToken):
        try:
            payload=jwt.decode(token,self.SECRET_KEY,algorithms=[self.ALGORITHM])
            sub=payload.get("sub")
            if sub is None : raise self.CREDENTIALS_EXCEPTION
            user=db.query(self.User).filter(or_(self.User.username==sub , self.User.email==sub)).first()
            if user is None: raise self.CREDENTIALS_EXCEPTION
            ACCESS_TOKEN_EXPIRE_MINUTESs=timedelta(self.ACCESS_TOKEN_EXPIRE_MINUTES_MINUTES)
            access_token=self.create_access_token(
                data={"sub":sub},expires_delta=ACCESS_TOKEN_EXPIRE_MINUTESs
            )
            return access_token
        except JWTError:
            raise self.CREDENTIALS_EXCEPTION
