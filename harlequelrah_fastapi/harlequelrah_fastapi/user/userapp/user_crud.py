from fastapi.responses import JSONResponse
from my_project.settings.database import authentication
from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from fastapi import Depends
from fastapi import HTTPException as HE
from fastapi import Response, status

from harlequelrah_fastapi.crud.user_crud_forgery import UserCrudForgery
User = authentication.User
UserCreate = authentication.UserCreateModel
UserUpdate = authentication.UserUpdateModel

userCrud = UserCrudForgery(authentication)
