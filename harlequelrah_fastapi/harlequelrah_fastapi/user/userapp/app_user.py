from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from harlequelrah_fastapi.authentication.token import Token, AccessToken, RefreshToken
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends
import userapp.user_crud as crud
from settings.database import authentication
from sqlalchemy.orm import Session
from typing import List
from settings.database import authentication
from harlequelrah_fastapi.authentication.authenticate import AUTHENTICATION_EXCEPTION
from harlequelrah_fastapi.user.userCrud import UserCrud

app_user = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Utilisateur non trouvé"}},
)
dependencies = [
    Depends(authentication.get_session),
    Depends(authentication.get_current_user),
]
UserCreateModel = authentication.UserCreateModel
UserUpdateModel = authentication.UserUpdateModel
UserPydanticModel = authentication.UserPydanticModel
UserLoginModel = authentication.UserLoginModel


usercrud=  UserCrud (authentication)
@app_user.get("/count-users")
async def count_users(db:Session=dependencies[0]):
    return await usercrud.get_count_users(db)


@app_user.get("/get-user/{credential}", response_model=UserPydanticModel)
async def get_user(credential: str, db: Session = dependencies[0]):
    if credential.isdigit():
        return await usercrud.get_user(db,credential)
    return await usercrud.get_user(db,sub=credential)


@app_user.get("/get-users", response_model=List[UserPydanticModel])
async def get_users(db: Session = dependencies[0]):
    return await usercrud.get_users(db)


@app_user.post("/create-user", response_model=UserPydanticModel)
async def create_user(user: UserCreateModel, db: Session = dependencies[0]):
        return await usercrud.create_user(user=user,db=db)


@app_user.delete("/delete-user/{id}")
async def delete_user(
    id: int, db: Session = dependencies[0], access_token=dependencies[1]
):
    return await usercrud.delete_user(id,db)


@app_user.put("/update-user/{id}", response_model=UserPydanticModel)
async def update_user(user: UserUpdateModel, id: int, db: Session = dependencies[0],access_token=dependencies[1]):
    return await usercrud.update_user(id,user, db)


@app_user.get("/current-user", response_model=UserPydanticModel)
async def get_current_user(
    access_token: str = dependencies[1],
):
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


@app_user.post("/refresh-token", response_model=AccessToken)
async def refresh_token(
    current_user: UserPydanticModel = Depends(authentication.get_current_user),
):
    data = {"sub": current_user.username}
    access_token = authentication.create_access_token(data)
    return access_token


@app_user.post("/get-refresh-token-with-access-token", response_model=AccessToken)
async def refresh_token(refresh_token: RefreshToken):
    access_token = authentication.refresh_token(refresh_token)
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
