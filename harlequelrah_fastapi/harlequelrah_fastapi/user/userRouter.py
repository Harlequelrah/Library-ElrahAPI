from typing import Annotated, List, Optional

from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from harlequelrah_fastapi.authentication.authenticate import Authentication
from harlequelrah_fastapi.authentication.token import AccessToken, RefreshToken, Token
from harlequelrah_fastapi.exception.auth_exception import AUTHENTICATION_EXCEPTION
from harlequelrah_fastapi.router.route_config import RouteConfig
from harlequelrah_fastapi.router.router_provider import CustomRouterProvider
from harlequelrah_fastapi.user.models import UserChangePasswordRequestModel, UserLoginRequestModel
from harlequelrah_fastapi.user.userCrud import UserCrudForgery
from sqlalchemy.orm import Session

class UserRouterProvider(CustomRouterProvider):
    USER_AUTH_ROUTES_NAME : List[str] = [
        "read-current-user",
        "tokenUrl",
        "get-refresh-token",
        "refresh-token",
        "login",
        "change-password",
    ]
    USER_AUTH_CONFIG: List[RouteConfig] = [
        RouteConfig(
            route_name="read-current-user",
            is_activated=True,
            is_protected=True,
            summary="read current user",
            description=" read current user informations",
        ),
        RouteConfig(
            route_name="tokenUrl",
            is_activated=True,
            summary="Swagger UI's scopes",
            description="provide scopes for Swagger UI operations",
        ),
        RouteConfig(
            route_name="get-refresh-token",
            is_activated=True,
            is_protected=True,
            summary="get refresh token",
            description="allow you to retrieve refresh token",
        ),
        RouteConfig(
            route_name="refresh-token",
            is_activated=True,
            summary="refresh token",
            description="refresh your access token with refresh token",
        ),
        RouteConfig(
            route_name="login",
            is_activated=True,
            summary="login",
            description="allow you to login",
        ),
        RouteConfig(
            route_name="change-password",
            is_activated=True,
            is_protected=True,
            summary="change password",
            description="allow you to change your password",
        ),
        RouteConfig(
            route_name="read-one",
            is_activated=True,
            is_protected=True,
            is_unlocked=True,
            summary="read one user",
            description="retrive one user from credential : id or email or username",
        ),
    ]

    def __init__(
        self,
        prefix: str,
        tags: List[str],
        crud: UserCrudForgery,
    ):
        self.authentication= crud.authentication
        super().__init__(
            prefix=prefix,
            tags=tags,
            PydanticModel=self.authentication.UserPydanticModel,
            crud=crud,
            get_access_token=self.authentication.get_access_token,
        )
        self.crud : UserCrudForgery = crud

    def get_default_router(self, exclude_routes_name: Optional[List[str]] = None):
        return super().get_default_router()

    def get_protected_router(self, exclude_routes_name: Optional[List[str]] = None):
        return super().get_protected_router()

    def initialize_router(self,init_data:List[RouteConfig]):
        self.router = super().initialize_router(init_data)
        for config in init_data:
            if config.route_path == "read-one" and config.is_activated and config.is_unlocked:

                @self.router.post(
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
                async def read_one_user(
                    credential : str|int):
                    return await self.crud.read_one(credential)
            if config.route_name == "read-current-user" and config.is_activated:
                @self.router.get(
                    path=config.route_path,
                    response_model=self.PydanticModel,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                )
                async def read_current_user(
                    current_user : self.PydanticModel = Depends(self.crud.get_current_user)
                    ):
                    return current_user

            if config.route_name == "tokenUrl" and config.is_activated:
                @self.router.post(
                    response_model=Token,
                    path=config.route_path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                )
                async def login_swagger(form_data:OAuth2PasswordRequestForm=Depends()):
                    user = await self.authentication.authenticate_user(form_data.username,form_data.password)
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
                    response_model=RefreshToken
                )
                async def refresh_token(current_user:self.PydanticModel=Depends(self.crud.get_current_user)):
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
                async def refresh_access_token(form_data: RefreshToken):
                    return await self.authentication.refresh_token(form_data.refresh_token)

            if config.route_name=='login' and config.is_activated:

                @self.router.post(
                    response_model=Token,
                    path=config.route_path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                )
                async def login(usermodel:UserLoginRequestModel):
                    user = await self.authentication.authenticate_user(usermodel.credential,usermodel.password)
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
                async def change_password(
                    form_data: UserChangePasswordRequestModel
                ):
                    credential = form_data.credential
                    old_password = form_data.current_password
                    new_password = form_data.new_password
                    return await self.crud.change_password(credential ,old_password,new_password)

        return self.router
