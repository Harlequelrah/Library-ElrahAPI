

from typing import List, Optional

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from elrahapi.authentication.authentication_manager import AuthenticationManager
from elrahapi.authentication.token import AccessToken, RefreshToken, Token
from elrahapi.router.route_config import AuthorizationConfig, RouteConfig,ResponseModelConfig
from elrahapi.router.router_crud import format_init_data, initialize_dependecies
from elrahapi.router.router_default_routes_name import DefaultRoutesName
from elrahapi.router.router_namespace import  USER_AUTH_CONFIG_ROUTES
from elrahapi.user.schemas import UserChangePasswordRequestModel, UserLoginRequestModel


class AuthenticationRouterProvider:
    def __init__(self,
                authentication:AuthenticationManager,
                with_relations:Optional[bool]=False,
                roles: Optional[List[str]] = None,
                privileges: Optional[List[str]] = None,
                ):

        self.authentication=authentication
        self.roles = roles
        self.privileges = privileges
        self.with_relations = with_relations


        self.router =APIRouter(
            prefix="/auth",
            tags=["auth"]
        )

    def get_auth_router(
        self,
        init_data: List[RouteConfig]=USER_AUTH_CONFIG_ROUTES,
        authorizations : Optional[List[AuthorizationConfig]]=None,
        exclude_routes_name: Optional[List[DefaultRoutesName]] = None,        response_model_configs: Optional[List[ResponseModelConfig]] = None,
        )->APIRouter:
        formatted_data = format_init_data(
            init_data=init_data,
            with_relations=self.with_relations,
            authorizations=authorizations,
            exclude_routes_name=exclude_routes_name,
            authentication=self.authentication,
            roles=self.roles,
            privileges=self.privileges,
            response_model_configs=response_model_configs,
            ReadPydanticModel=self.authentication.authentication_models.read_model
            ,FullReadPydanticModel=self.authentication.authentication_models.full_read_model
        )
        for config in formatted_data:
            if config.route_name == DefaultRoutesName.READ_ONE_USER :
                @self.router.get(
                    path=config.route_path,
                    response_model=config.response_model ,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    dependencies=config.dependencies
                )
                async def read_one_user(username_or_email: str):
                    return await self.authentication.read_one_user(username_or_email)
            if config.route_name == DefaultRoutesName.READ_CURRENT_USER :
                @self.router.get(
                    path=config.route_path,
                    response_model= config.response_model ,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    dependencies=config.dependencies
                )
                async def read_current_user(
                    current_user = Depends(
                        self.authentication.get_current_user
                    )
                ):
                    return current_user

            if config.route_name == DefaultRoutesName.TOKEN_URL :

                @self.router.post(
                    response_model=Token,
                    path=config.route_path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    dependencies=config.dependencies
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

            if config.route_name == DefaultRoutesName.GET_REFRESH_TOKEN :

                @self.router.post(
                    path=config.route_path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    response_model=RefreshToken,
                    dependencies=config.dependencies,
                )
                async def refresh_token(
                    current_user = Depends(
                        self.authentication.get_current_user
                    ),
                ):
                    data = {"sub": current_user.username}
                    refresh_token = self.authentication.create_refresh_token(data)
                    return refresh_token

            if config.route_name == DefaultRoutesName.REFRESH_TOKEN :
                @self.router.post(
                    path=config.route_path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    response_model=AccessToken,
                    dependencies=config.dependencies,
                )
                async def refresh_access_token(refresh_token: RefreshToken):
                    return await self.authentication.refresh_token(
                        refresh_token_data=refresh_token
                    )

            if config.route_name == DefaultRoutesName.LOGIN :

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

            if config.route_name == DefaultRoutesName.CHANGE_PASSWORD :
                @self.router.post(
                    status_code=204,
                    path=config.route_path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    dependencies=config.dependencies,
                )
                async def change_password(form_data: UserChangePasswordRequestModel):
                    username_or_email = form_data.username_or_email
                    current_password = form_data.current_password
                    new_password = form_data.new_password
                    return await self.authentication.change_password(
                        username_or_email, current_password, new_password
                    )

        return self.router




