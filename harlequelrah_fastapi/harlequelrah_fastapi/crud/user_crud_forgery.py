from typing import Optional
from fastapi.responses import JSONResponse
from harlequelrah_fastapi.authentication.authenticate import Authentication
from harlequelrah_fastapi.crud.crud_forgery import CrudForgery
from harlequelrah_fastapi.exception.custom_http_exception import (
    CustomHttpException as CHE,
)
from harlequelrah_fastapi.exception.exceptions_utils import raise_custom_http_exception
from harlequelrah_fastapi.utility.utils import update_entity
from sqlalchemy import or_
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import HTTPException as HE
from fastapi import status


class UserCrudForgery(CrudForgery):
    def __init__(self, authentication: Authentication):
        super().__init__(
            entity_name="user",
            session_factory=authentication.session_factory,
            SQLAlchemyModel=authentication.User,
            CreatePydanticModel=authentication.UserCreateModel,
            UpdatePydanticModel=authentication.UserUpdateModel,
        )
        self.authentication = authentication
        self.get_current_user: callable = authentication.get_current_user

    async def change_password(
        self, credential: str, current_password: str, new_password: str
    ):
        session = self.authentication.get_session()
        current_user = await self.authentication.authenticate_user(
            password=current_password, username_or_email=credential, session=session
        )
        if current_user.check_password(current_password):
            current_user.set_password(new_password)
            session.commit()
            session.refresh(current_user)
            return JSONResponse(
                status_code=200,
                content={"message": "Password updated successfully"},
            )
        else:
            raise_custom_http_exception(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Your current password you enter  is incorrect"
            )


    async def is_unique(self, sub: str):
        db = self.session_factory()
        user = (
            db.query(self.SQLAlchemyModel)
            .filter(
                or_(
                    self.SQLAlchemyModel.email == sub,
                    self.SQLAlchemyModel.username == sub,
                )
            )
            .first()
        )
        return user is None

    async def read_one(self, credential: int | str, db: Optional[Session] = None):
        user = None
        if db:
            session = db
        else:
            session = self.session_factory()
        if isinstance(credential, int):
            user = await super().read_one(id, db=session)
        elif isinstance(credential, str):
            user = (
                session.query(self.SQLAlchemyModel)
                .filter(
                    or_(
                        self.SQLAlchemyModel.username == credential,
                        self.SQLAlchemyModel.email == credential,
                    )
                )
                .first()
            )
            if not user:
                detail = (
                    f"{self.entity_name} with username or email {credential} not found"
                )
                http_exc = HE(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
                custom_http_exception = CHE(http_exc)
                raise custom_http_exception
        return user
