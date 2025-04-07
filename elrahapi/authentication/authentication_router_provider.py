

from typing import List, Optional

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from elrahapi.authentication.authentication_manager import AuthenticationManager
from elrahapi.authentication.token import AccessToken, RefreshToken, Token
from elrahapi.router.route_config import AuthorizationConfig, RouteConfig
from elrahapi.router.router_crud import format_init_data, initialize_dependecies
from elrahapi.router.router_default_routes_name import DefaultRoutesName
from elrahapi.router.router_namespace import  USER_AUTH_CONFIG_ROUTES
from elrahapi.user.schemas import UserChangePasswordRequestModel, UserLoginRequestModel


class AuthenticationRouterProvider:
    def __init__(self,authentication:AuthenticationManager):

        self.authentication=authentication

        self.pydantic_model = authentication.authentication_models.pydantic_model

        self.router =APIRouter(
            prefix="/auth",
            tags=["auth"]
        )

    def get_auth_router(
        self,
        init_data: List[RouteConfig]=USER_AUTH_CONFIG_ROUTES,
        authorizations : Optional[List[AuthorizationConfig]]=None,
        exclude_routes_name: Optional[List[DefaultRoutesName]] = None,
        )->APIRouter:
        formatted_init_data = format_init_data(
            init_data=init_data,
            authorizations=authorizations,
            exclude_routes_name=exclude_routes_name
        )
        for config in formatted_init_data:
            if config.route_name == DefaultRoutesName.READ_ONE_USER and config.is_activated:
                dependencies = initialize_dependecies(
                    config=config,
                    authentication=self.authentication,
                )
                @self.router.get(
                    path=config.route_path,
                    response_model=self.pydantic_model,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    dependencies=dependencies
                )
                async def read_one_user(username_or_email: str):
                    return await self.authentication.read_one_user(username_or_email)
            if config.route_name == DefaultRoutesName.READ_CURRENT_USER and config.is_activated:
                @self.router.get(
                    path=config.route_path,
                    response_model=self.pydantic_model,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                )
                async def read_current_user(
                    current_user = Depends(
                        self.authentication.get_current_user
                    )
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
                        "sub": user.username,
                        "roles": [user_role.role.normalizedName for user_role in user.user_roles]
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
                    current_user = Depends(
                        self.authentication.get_current_user
                    ),
                ):
                    data = {"sub": current_user.username}
                    refresh_token = self.authentication.create_refresh_token(data)
                    return refresh_token

            if config.route_name == DefaultRoutesName.REFRESH_TOKEN and config.is_activated:
                dependencies = initialize_dependecies(
                    config=config,
                    authentication=self.authentication,
                )

                @self.router.post(
                    path=config.route_path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    response_model=AccessToken,
                    dependencies=dependencies,
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
                        "roles": [user_role.role.normalizedName for user_role in user.user_roles]
                    }
                    access_token_data = self.authentication.create_access_token(data)
                    refresh_token_data = self.authentication.create_refresh_token(data)
                    return {
                        "access_token": access_token_data.get("access_token"),
                        "refresh_token": refresh_token_data.get("refresh_token"),
                        "token_type": "bearer",
                    }

            if config.route_name == DefaultRoutesName.CHANGE_PASSWORD and config.is_activated:
                dependencies = initialize_dependecies(
                    config=config,
                    authentication=self.authentication,
                )

                @self.router.post(
                    status_code=204,
                    path=config.route_path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    dependencies=dependencies,
                )
                async def change_password(form_data: UserChangePasswordRequestModel):
                    username_or_email = form_data.username_or_email
                    current_password = form_data.current_password
                    new_password = form_data.new_password
                    return await self.authentication.change_password(
                        username_or_email, current_password, new_password
                    )

        return self.router




