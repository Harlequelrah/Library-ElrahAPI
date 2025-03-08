from typing import List, Optional

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from elrahapi.authentication.token import AccessToken, RefreshToken, Token

from elrahapi.router.route_config import AuthorizationConfig, RouteConfig
from elrahapi.router.router_crud import exclude_route, initialize_dependecies
from elrahapi.router.router_namespace import (
    DefaultRoutesName,
    ROUTES_PROTECTED_CONFIG,
    ROUTES_PUBLIC_CONFIG,
    USER_AUTH_CONFIG_ROUTES,
)
from elrahapi.router.router_provider import CustomRouterProvider
from elrahapi.user.models import (
    UserChangePasswordRequestModel,
    UserLoginRequestModel,
)
from elrahapi.crud.user_crud_forgery import UserCrudForgery



class UserRouterProvider(CustomRouterProvider):

    def __init__(
        self,
        prefix: str,
        tags: List[str],
        crud: UserCrudForgery,
        roles : Optional[List[str]]=None,
        privileges : Optional[List[str]]=None,
    ):
        self.authentication = crud.authentication
        super().__init__(
            prefix=prefix,
            tags=tags,
            PydanticModel=self.authentication.UserPydanticModel,
            crud=crud,
            roles=roles,
            privileges=privileges
        )
        self.crud: UserCrudForgery = crud

    def get_public_router(
        self, exclude_routes_name: Optional[List[DefaultRoutesName]] = None
    ) -> APIRouter:
        routes = USER_AUTH_CONFIG_ROUTES + exclude_route(
            ROUTES_PUBLIC_CONFIG, [DefaultRoutesName.READ_ONE]
        )
        return self.initialize_router(routes, exclude_routes_name)

    def get_protected_router(
        self,authorizations:Optional[List[AuthorizationConfig]]=None,  exclude_routes_name: Optional[List[DefaultRoutesName]] = None
    ) -> APIRouter:
        routes = USER_AUTH_CONFIG_ROUTES + exclude_route(
            ROUTES_PROTECTED_CONFIG, [DefaultRoutesName.READ_ONE]
        )
        return self.initialize_router(
            init_data=routes,
            authorizations=authorizations,
            exclude_routes_name=exclude_routes_name)

    def initialize_router(
        self,
        init_data: List[RouteConfig],
        authorizations:Optional[List[AuthorizationConfig]]=None,
        exclude_routes_name: Optional[List[DefaultRoutesName]] = None,
    ):
        self.router = super().initialize_router(
            init_data=init_data,
            authorizations=authorizations,
            exclude_routes_name=exclude_routes_name
            )
        for config in init_data:
            if config.route_name == DefaultRoutesName.READ_ONE_USER and config.is_activated:
                dependencies= initialize_dependecies(
                    config=config,
                    authentication= self.crud.authentication,
                    roles=self.roles,
                    privileges = self.privileges
                )

                @self.router.get(
                    path=config.route_path,
                    response_model=self.PydanticModel,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    dependencies = dependencies
                )
                async def read_one_user(username_or_email: str):
                    return await self.crud.read_one_user(username_or_email)

            if config.route_name == DefaultRoutesName.READ_CURRENT_USER and config.is_activated:

                @self.router.get(
                    # name=config.route_name.value,
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

            if config.route_name == DefaultRoutesName.TOKEN_URL and config.is_activated:

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
                        password=form_data.password,
                        username_or_email=form_data.username,
                    )

                    data = {
                        "sub": form_data.username,
                        "role": user.role.normalizedName if user.role else "NO ROLE",
                    }
                    access_token = self.authentication.create_access_token(data)
                    refresh_token = self.authentication.create_refresh_token(data)
                    return {
                        "access_token": access_token["access_token"],
                        "refresh_token": refresh_token["refresh_token"],
                        "token_type": "bearer",
                    }

            if config.route_name == DefaultRoutesName.GET_REFRESH_TOKEN and config.is_activated:

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

            if config.route_name == DefaultRoutesName.REFRESH_TOKEN and config.is_activated:

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

            if config.route_name == DefaultRoutesName.LOGIN and config.is_activated:

                @self.router.post(
                    response_model=Token,
                    path=config.route_path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                )
                async def login(usermodel: UserLoginRequestModel):
                    username_or_email = usermodel.username_or_email
                    user = await self.authentication.authenticate_user(
                        usermodel.password, username_or_email
                    )
                    data = {
                        "sub": username_or_email,
                        "role": user.role.normalizedName if user.role else "NO ROLE",
                    }
                    access_token_data = self.authentication.create_access_token(data)
                    refresh_token_data = self.authentication.create_refresh_token(data)
                    return {
                        "access_token": access_token_data.get("access_token"),
                        "refresh_token": refresh_token_data.get("refresh_token"),
                        "token_type": "bearer",
                    }

            if config.route_name == DefaultRoutesName.CHANGE_PASSWORD and config.is_activated:

                @self.router.post(
                    status_code=204,
                    path=config.route_path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                )
                async def change_password(form_data: UserChangePasswordRequestModel):
                    username_or_email = form_data.username_or_email
                    current_password = form_data.current_password
                    new_password = form_data.new_password
                    return await self.crud.change_password(
                        username_or_email, current_password, new_password
                    )

        return self.router
