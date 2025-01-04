from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from harlequelrah_fastapi.authentication.authenticate import Authentication
from harlequelrah_fastapi.authentication.token import AccessToken, RefreshToken, Token
from harlequelrah_fastapi.exception.auth_exception import (
    INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION,
)
from harlequelrah_fastapi.router.route_config import RouteConfig
from harlequelrah_fastapi.router.router_crud import exclude_route
from harlequelrah_fastapi.router.router_namespace import (
    DEFAULTROUTESNAME,
    ROUTES_PROTECTED_CONFIG,
    ROUTES_PUBLIC_CONFIG,
    USER_AUTH_CONFIG_ROUTES,
)
from harlequelrah_fastapi.router.router_provider import CustomRouterProvider
from harlequelrah_fastapi.user.models import (
    UserChangePasswordRequestModel,
    UserLoginRequestModel,
)
from harlequelrah_fastapi.user.userCrud import UserCrudForgery
from sqlalchemy.orm import Session


class UserRouterProvider(CustomRouterProvider):

    def __init__(
        self,
        prefix: str,
        tags: List[str],
        crud: UserCrudForgery,
    ):
        self.authentication = crud.authentication
        super().__init__(
            prefix=prefix,
            tags=tags,
            PydanticModel=self.authentication.UserPydanticModel,
            crud=crud,
            get_access_token=self.authentication.get_access_token,
        )
        self.crud: UserCrudForgery = crud

    def get_public_router(
        self, exclude_routes_name: Optional[List[DEFAULTROUTESNAME]] = None
    ) -> APIRouter:
        routes = USER_AUTH_CONFIG_ROUTES + exclude_route(
            ROUTES_PUBLIC_CONFIG, [DEFAULTROUTESNAME.READ_ONE]
        )
        return self.initialize_router(routes, exclude_routes_name)

    def get_protected_router(
        self, exclude_routes_name: Optional[List[DEFAULTROUTESNAME]] = None
    ) -> APIRouter:
        routes = USER_AUTH_CONFIG_ROUTES + exclude_route(
            ROUTES_PROTECTED_CONFIG, [DEFAULTROUTESNAME.READ_ONE]
        )
        return self.initialize_router(routes, exclude_routes_name)

    def initialize_router(
        self,
        init_data: List[RouteConfig],
        exclude_routes_name: Optional[List[DEFAULTROUTESNAME]] = None,
    ):
        self.router = super().initialize_router(init_data, exclude_routes_name)
        for config in init_data:
            if (
                config.route_name == "read-one"
                and config.is_activated
                and config.is_unlocked
            ):

                @self.router.get(
                    path=config.route_path,
                    response_model=self.PydanticModel,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    dependencies=(
                        [Depends(self.get_access_token)]
                        if self.get_access_token and config.is_protected
                        else []
                    ),
                )
                async def read_one_user(credential: str | int):
                    return await self.crud.read_one(credential)

            if config.route_name == "read-current-user" and config.is_activated:

                @self.router.get(
                    path=config.route_path,
                    response_model=self.PydanticModel,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                )
                async def read_current_user(
                    current_user: self.PydanticModel = Depends(
                        self.crud.get_current_user
                    ),
                ):
                    return current_user

            if config.route_name == "tokenUrl" and config.is_activated:

                @self.router.post(
                    response_model=Token,
                    path=config.route_path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                )
                async def login_swagger(
                    form_data: OAuth2PasswordRequestForm = Depends(),
                ):
                    user = await self.authentication.authenticate_user(
                        form_data.password, form_data.username
                    )
                    data = {"sub": user.username}
                    access_token = self.authentication.create_access_token(data)
                    refresh_token = self.authentication.create_refresh_token(data)

                    return {
                        "access_token": access_token["access_token"],
                        "refresh_token": refresh_token["refresh_token"],
                        "token_type": "bearer",
                    }

            if config.route_name == "get-refresh-token" and config.is_activated:

                @self.router.post(
                    path=config.route_path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    response_model=RefreshToken,
                )
                async def refresh_token(
                    current_user: self.PydanticModel = Depends(
                        self.crud.get_current_user
                    ),
                ):
                    data = {"sub": current_user.username}
                    refresh_token = self.authentication.create_refresh_token(data)
                    return refresh_token

            if config.route_name == "refresh-token" and config.is_activated:

                @self.router.post(
                    path=config.route_path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    response_model=AccessToken,
                )
                async def refresh_access_token(refresh_token: RefreshToken):
                    return await self.authentication.refresh_token(
                        refresh_token_data=refresh_token
                    )

            if config.route_name == "login" and config.is_activated:

                @self.router.post(
                    response_model=Token,
                    path=config.route_path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                )
                async def login(usermodel: UserLoginRequestModel):
                    credential = (
                        usermodel.username if usermodel.username else usermodel.email
                    )
                    user = await self.authentication.authenticate_user(
                    usermodel.password, credential
                    )
                    data = {"sub": usermodel.credential}
                    access_token_data = self.authentication.create_access_token(data)
                    refresh_token_data = self.authentication.create_refresh_token(data)
                    return {
                        "access_token": access_token_data.get("access_token"),
                        "refresh_token": refresh_token_data.get("refresh_token"),
                        "token_type": "bearer",
                    }

            if config.route_name == "change-password" and config.is_activated:

                @self.router.post(
                    response_model=Token,
                    path=config.route_path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                )
                async def change_password(form_data: UserChangePasswordRequestModel):
                    credential = form_data.credential
                    old_password = form_data.current_password
                    new_password = form_data.new_password
                    return await self.crud.change_password(
                        credential, old_password, new_password
                    )

        return self.router
