from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import HTTPException as HE, Response, status, Depends
from myproject.settings.database import authentication
from sqlalchemy import or_
from harlequelrah_fastapi.utility.utils import update_entity
from harlequelrah_fastapi.user.userCrud import  UserCrudForgery

userCrud = UserCrudForgery(authentication)

async def get_count_users(db: Session):
    pass


async def is_unique(sub: str, db: Session):
    pass


async def create_user(
    user: authentication.UserCreate,
    db: Session,
):
    pass


async def get_user(
    db: Session ,
    id: int = None,
    sub: str = None,
): pass


async def get_users(
    db: Session,
    skip: int = 0,
    limit: int = None,
):pass

async def delete_user(user_id:int,db:Session):
    pass

async def update_user(
    db: Session,
    user_id: int,
    user: authentication.UserUpdate,
):pass
