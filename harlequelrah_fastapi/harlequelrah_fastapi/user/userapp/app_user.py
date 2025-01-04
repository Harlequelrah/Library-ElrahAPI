from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from harlequelrah_fastapi.authentication.token import Token, AccessToken, RefreshToken
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends
# import myproject.userapp.user_crud as crud
from harlequelrah_fastapi.router.router_namespace import DEFAULTROUTESNAME, USER_AUTH_CONFIG
from myproject.settings.database import authentication
from sqlalchemy.orm import Session
from typing import List
# from myproject.settings.database import authentication
from harlequelrah_fastapi.authentication.authenticate import AUTHENTICATION_EXCEPTION
from .user_crud import userCrud

from harlequelrah_fastapi.user.userRouter import UserRouterProvider

user_router_provider = UserRouterProvider(
    prefix="/users",
    tags=["users"],
    crud=userCrud,
)
app_user = user_router_provider.get_mixed_router(
    init_data=USER_AUTH_CONFIG,
    public_routes_name=[DEFAULTROUTESNAME.CREATE],
    protected_routes_name=[DEFAULTROUTESNAME.READ_ALL_BY_FILTER],
)
