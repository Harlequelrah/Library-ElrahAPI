from sqlalchemy.orm import Session
from fastapi import  Depends, HTTPException, status
from harlequelrah_fastapi.authentication.token import Token, AccessToken, RefreshToken
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends
from settings.database import get_db
from sqlalchemy.orm import Session
import user_crud as crud
from typing import List


from settings.secret import authentication
app_user = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Utilisateur non trouvé"}},
)
User = authentication.User
UserLoginModel = authentication.User
UserCreate=authentication.UserCreateModel
UserUpdate=authentication.UserUpdateModel
async def get_current_user():
    await authentication.get_current_user()


AUTHENTICATION_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid email/username or password",
    headers={"WWW-Authenticate": "Beaer"},
)

@app_user.get("/count-users")
async def count_users(db: Session = Depends(get_db)):
    return await crud.get_count_users(db)


@app_user.get("/get-user/{credential}", response_model=User)
async def get_user(
    credential: str,
    db: Session = Depends(get_db),
    access_token: str = Depends(get_current_user),
):
    if credential.isdigit():
        return await crud.get_user(id=credential)
    return await crud.get_user(sub=credential, db=db)


@app_user.get("/get-users", response_model=List[User])
async def get_users(
    access_token: str = Depends(get_current_user), db: Session = Depends(get_db)
):
    return await crud.get_users(db)


@app_user.post("/create-user", response_model=User)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    access_token: str = Depends(get_current_user),
):
    return await crud.create_user(user, db)


@app_user.delete("/delete-user/{id}")
async def delete_user(
    id: int,
    db: Session = Depends(get_db),
    access_token: str = Depends(get_current_user),
):
    return await crud.delete_user(id, db)


@app_user.put("/update-user/{id}", response_model=User)
async def update_user(
    user: UserUpdate,
    id: int,
    db: Session = Depends(get_db),
    access_token: str = Depends(get_current_user),
):
    return await crud.update_user(id, user, db)


@app_user.get("/current-user", response_model=User)
async def get_current_user(access_token: str = Depends(get_current_user)):
    return access_token


@app_user.post("/tokenUrl", response_model=Token)
async def login_api_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = await authentication.authenticate_user(
        db, form_data.username, form_data.password
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


@app_user.get("/refresh-token", response_model=AccessToken)
async def refresh_token(refresh_token: RefreshToken):
    access_token = authentication.refresh_token(refresh_token)
    return access_token


@app_user.get("/refresh-token", response_model=AccessToken)
async def refresh_token(current_user: User = Depends(authentication.get_current_user)):
    data = {"sub": current_user.username}
    access_token = authentication.create_access_token(data)
    return access_token


@app_user.post("/login", response_model=Token)
async def login(usermodel: UserLoginModel, db: Session = Depends(get_db)):
    if (usermodel.email is None) ^ (usermodel.username is None):
        credential = usermodel.username if usermodel.username else usermodel.email
        user = await authentication.authenticate_user(
            db, credential, usermodel.password
        )
        if not user:
            raise AUTHENTICATION_EXCEPTION
        data = {"sub": credential}
        access_token = authentication.create_access_token(data)
        refresh_token = authentication.create_refresh_token(data)
        return {
            "access_token": access_token["access_token"],
            "refresh_token": refresh_token["refresh_token"],
            "token_type": "bearer",
        }
    else:
        raise AUTHENTICATION_EXCEPTION
