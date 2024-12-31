from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from harlequelrah_fastapi.authentication.token import Token, AccessToken, RefreshToken
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends
# import myproject.userapp.user_crud as crud
from myproject.settings.database import authentication
from sqlalchemy.orm import Session
from typing import List
# from myproject.settings.database import authentication
from harlequelrah_fastapi.authentication.authenticate import AUTHENTICATION_EXCEPTION
from .user_crud import usercrud

app_user = APIRouter(
    prefix="/users",
    tags=["users"],
)
token_dependency = Depends(authentication.get_access_token)
UserCreateModel = authentication.UserCreateModel
UserUpdateModel = authentication.UserUpdateModel
UserPydanticModel = authentication.UserPydanticModel
UserLoginModel = authentication.UserLoginModel



@app_user.get("/count-users")
async def count_users(access_token: str = token_dependency):
    return await usercrud.get_count_users()


@app_user.get("/get-user/{credential}", response_model=UserPydanticModel)
async def get_user(credential: str, access_token: str = token_dependency):
    if credential.isdigit():
        return await usercrud.get_user(credential)
    return await usercrud.get_user(sub=credential)


@app_user.get("/get-users", response_model=List[UserPydanticModel])
async def get_users(access_token: str = token_dependency):
    return await usercrud.get_users()


@app_user.post("/create-user", response_model=UserPydanticModel)
async def create_user(user: UserCreateModel):
    return await usercrud.create_user(user=user)


@app_user.delete("/delete-user/{id}")
async def delete_user(id: int, access_token: str = token_dependency):
    return await usercrud.delete_user(id)


@app_user.put("/update-user/{id}", response_model=UserPydanticModel)
async def update_user(
    user: UserUpdateModel, id: int, access_token: str = token_dependency
):
    return await usercrud.update_user(id, user)


@app_user.get("/current-user", response_model=UserPydanticModel)
async def get_current_user(access_token: str = token_dependency):
    return access_token


@app_user.post("/tokenUrl", response_model=Token)
async def login_api_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authentication.authenticate_user(
        form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email/username or password",
            headers={"WWW-Authenticate": "Beaer"},
        )
    data = {"sub": form_data.username}
    access_token = authentication.create_access_token(data)
    refresh_token = authentication.create_refresh_token(data)

    return {
        "access_token": access_token["access_token"],
        "refresh_token": refresh_token["refresh_token"],
        "token_type": "bearer",
    }


@app_user.post("/get-refresh-token", response_model=RefreshToken)
async def refresh_token(
    current_user: UserPydanticModel = Depends(authentication.get_current_user),
):
    data = {"sub": current_user.username}
    refresh_token = authentication.create_refresh_token(data)
    return refresh_token


@app_user.post("/refresh-token", response_model=AccessToken)
async def refresh_token(refresh_token: RefreshToken):
    access_token = authentication.create_refresh_token(refresh_token)
    return access_token


@app_user.post("/login", response_model=Token)
async def login(usermodel: UserLoginModel):
    if (usermodel.email is None) ^ (usermodel.username is None):
        credential = usermodel.username if usermodel.username else usermodel.email
        user = await authentication.authenticate_user(credential, usermodel.password)
        if not user:
            raise AUTHENTICATION_EXCEPTION
        data = {"sub": credential}
        access_token_data = authentication.create_access_token(data)
        refresh_token_data = authentication.create_refresh_token(data)
        return {
            "access_token": access_token_data.get("access_token"),
            "refresh_token": refresh_token_data.get("refresh_token"),
            "token_type": "bearer",
        }
    else:
        raise AUTHENTICATION_EXCEPTION
