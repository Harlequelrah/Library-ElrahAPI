from fastapi import  Depends, HTTPException, status
from harlequelrah_fastapi.authentication.token import Token, AccessToken, RefreshToken
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends
import harlequelrah_fastapi.user.userapp.user_crud as crud
from typing import List
from settings.database import authentication
from harlequelrah_fastapi.authentication.authenticate import AUTHENTICATION_EXCEPTION
app_user = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Utilisateur non trouvé"}},
)

UserCreateModel=authentication.UserCreateModel
UserUpdateModel=authentication.UserUpdateModel
UserPydanticModel=authentication.UserPydanticModel
UserLoginModel=authentication.UserLoginModel

@app_user.get("/count-users",response_model=List[UserPydanticModel])
async def count_users():
    return await crud.get_count_users()


@app_user.get("/get-user/{credential}", response_model=authentication.UserPydanticModel)
async def get_user(
    credential: str,


):
    if credential.isdigit():
        return await crud.get_user(id=credential)
    return await crud.get_user(sub=credential)


@app_user.get("/get-users", response_model=List[authentication.UserPydanticModel])
async def get_users():
    return await crud.get_users()


@app_user.post("/create-user", response_model=authentication.UserPydanticModel)
async def create_user(
    user: UserCreateModel,
):
    return await crud.create_user(user)


@app_user.delete("/delete-user/{id}")
async def delete_user(
    id: int
):
    return await crud.delete_user(id)


@app_user.put("/update-user/{id}", response_model=authentication.UserPydanticModel)
async def update_user(
    user: UserUpdateModel ,
    id: int
):
    return await crud.update_user(id, user)


@app_user.get("/current-user", response_model=authentication.UserPydanticModel)
async def get_current_user(access_token: str = Depends(authentication.get_current_user)):
    return access_token


@app_user.post("/tokenUrl", response_model=Token)
async def login_api_user(
    form_data: OAuth2PasswordRequestForm = Depends()
):
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
        "access_token": access_token.access_token,
        "refresh_token": refresh_token.refresh_token,
        "token_type": "bearer",
    }


@app_user.post("/refresh-token", response_model=AccessToken)
async def refresh_token(current_user: UserPydanticModel = Depends(authentication.get_current_user)):
    data = {"sub": current_user.username}
    access_token = authentication.create_access_token(data)
    return access_token


@app_user.post("/refresh-token-with-access-token", response_model=AccessToken)
async def refresh_token(refresh_token: RefreshToken):
    access_token = authentication.refresh_token( refresh_token)
    return access_token


@app_user.post("/login", response_model=Token)
async def login(usermodel: UserLoginModel):
    if (usermodel.email is None) ^ (usermodel.username is None):
        credential = usermodel.username if usermodel.username else usermodel.email
        user = await authentication.authenticate_user(
            credential, usermodel.password
        )
        if not user:
            raise AUTHENTICATION_EXCEPTION
        data = {"sub": credential}
        access_token_data = authentication.create_access_token(data)
        refresh_token_data = authentication.create_refresh_token(data)
        return {"access_token": access_token_data.access_token,
                "refresh_token": refresh_token_data.refresh_token,
                "token_type":"bearer"}

    else:
        raise AUTHENTICATION_EXCEPTION
