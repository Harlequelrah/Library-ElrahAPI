from fastapi.responses import JSONResponse
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from fastapi import HTTPException as HE, Response, status, Depends
from settings.database import authentication
from sqlalchemy import or_
from harlequelrah_fastapi.utility.utils import update_entity
from harlequelrah_fastapi.authentication.authenticate import Authentication


class UserCrud:
    def __init__(self, authentication: Authentication):
        self.authentication = authentication
        self.User = self.authentication.User
        self.UserLoginModel = self.authentication.UserLoginModel
        self.UserCreate = self.authentication.UserCreateModel
        self.UserUpdate = self.authentication.UserUpdateModel

    async def get_count_users(self,db:Session):
        return db.query(func.count(self.User.id)).scalar()

    async def is_unique(self, sub: str,db:Session):
        user = (
            db.query(self.User)
            .filter(or_(self.User.email == sub, self.User.username == sub))
            .first()
        )
        return user is None

    async def create_user(self, user, db: Session):
        new_user = self.User(**user.dict())
        if not await self.is_unique(new_user.email,db) or not await self.is_unique(
            new_user.username,db
        ):
            print("wakawaka")
            raise HE(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already registred",
            )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    async def get_user(self,db:Session,id: int = None,sub: str = None):
        user = (
            db.query(self.User)
            .filter(
                or_(
                    self.User.username == sub,
                    self.User.email == sub,
                    self.User.id == id,
                )
            )
            .first()
        )
        return user

    async def get_users(
        self,
        db: Session ,
        skip: int = 0,
        limit: int = None,
    ):
        limit = await self.get_count_users(db)
        users = db.query(self.User).offset(skip).limit(limit).all()
        return users

    async def update_user(self,
        user_id: int,
        userUpdated,
        db: Session ,
    ):
        existing_user = await self.get_user(db, user_id)
        update_entity(existing_user, userUpdated)
        db.commit()
        db.refresh(existing_user)
        return existing_user

    async def delete_user(self,user_id:int,db:Session):
        user = await self.get_user(db,id=user_id)
        db.delete(user)
        db.commit()
        return JSONResponse(status_code=200,content={'message': 'User deleted successfully'})
