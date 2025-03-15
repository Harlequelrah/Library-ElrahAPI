from typing import Optional
from elrahapi.authentication.authentication_manager import AuthenticationManager
from elrahapi.crud.crud_forgery import CrudForgery

from elrahapi.exception.exceptions_utils import raise_custom_http_exception
from sqlalchemy import or_
from fastapi import status


class UserCrudForgery(CrudForgery):
    def __init__(self,authentication: AuthenticationManager):
        super().__init__(
        session_factory=authentication.authentication_provider.session_factory,
        )
        self.authentication = authentication
        self.SQLAlchemyModel = authentication.crud_model.sqlalchemy_model
        self.entity_name = authentication.crud_model.entity_name
    async def change_password(
        self, username_or_email: str, current_password: str, new_password: str
    ):
        session = self.session_factory()
        current_user = await self.authentication.authenticate_user(
            password=current_password,
            username_or_email=username_or_email,
            session=session,
        )
        if current_user.check_password(current_password):
            current_user.set_password(new_password)
            session.commit()
            session.refresh(current_user)
        else:
            raise_custom_http_exception(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Your current password you enter  is incorrect",
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

    async def read_one_user(self,username_or_email:str):
        session = self.session_factory()
        user = (
            session.query(self.SQLAlchemyModel)
            .filter(
                or_(
                    self.SQLAlchemyModel.username == username_or_email,
                    self.SQLAlchemyModel.email == username_or_email,
                )
            )
            .first()
        )
        if not user:
            detail = f"{self.entity_name} with username or email {username_or_email} not found"
            raise_custom_http_exception(
                status_code=status.HTTP_404_NOT_FOUND, detail=detail
            )
        return user


