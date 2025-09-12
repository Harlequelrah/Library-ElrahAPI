from typing import Type

from elrahapi.authentication.authentication_manager import AuthenticationManager
from elrahapi.router.route_config import (
    AuthorizationConfig,
    ResponseModelConfig,
    RouteConfig,
)
from elrahapi.router.router_namespace import (
    DEFAULT_ROUTES_CONFIGS,
    USER_AUTH_CONFIG,
    DefaultRouteConfig,
    TypeRoute,
)
from elrahapi.router.router_routes_name import (
    DefaultRoutesName,
    RoutesName,
)
from pydantic import BaseModel

from fastapi import Depends


def exclude_route(
    routes: list[RouteConfig],
    exclude_routes_name: list[RoutesName] | None = None,
):
    init_data: list[RouteConfig] = []
    if exclude_routes_name:
        for route in routes:
            if route.route_name not in exclude_routes_name and route.is_activated:
                init_data.append(route)
    return init_data if init_data else routes


def get_single_route(
    route_name: DefaultRoutesName, type_route: TypeRoute | None = TypeRoute.PUBLIC
) -> RouteConfig:
    config: DefaultRouteConfig = DEFAULT_ROUTES_CONFIGS.get(route_name)
    if config:
        return RouteConfig(
            route_name=route_name,
            is_activated=True,
            summary=config.summary,
            description=config.description,
            is_protected=type_route == TypeRoute.PROTECTED,
        )
    else:
        return USER_AUTH_CONFIG[route_name]


def initialize_dependecies(
    config: RouteConfig,
    authentication: AuthenticationManager = None,
    roles: list[str] = None,
    privileges: list[str] = None,
):
    if not authentication:
        return []
    dependencies = []
    if config.is_protected:
        if roles:
            for role in roles:
                config.roles.append(role)
        if privileges:
            for privilege in privileges:
                config.privileges.append(privilege)
        if config.roles or config.privileges:
            authorizations: list[callable] = config.get_authorizations(
                authentication=authentication
            )
            dependencies: list[Depends] = [
                Depends(authorization) for authorization in authorizations
            ]
        else:
            dependencies = [Depends(authentication.get_access_token)]
    return dependencies


def add_authorizations(
    routes_config: list[RouteConfig], authorizations: list[AuthorizationConfig]
):
    authorized_routes_config: list[RouteConfig] = []
    for route_config in routes_config:
        authorization = next(
            (
                authorization
                for authorization in authorizations
                if authorization.route_name == route_config.route_name
                and route_config.is_protected
            ),
            None,
        )
        if authorization:
            route_config.extend_authorization_config(authorization)
        authorized_routes_config.append(route_config)
    return authorized_routes_config


def set_response_models(
    routes_config: list[RouteConfig],
    response_model_configs: list[ResponseModelConfig] | None,
    read_with_relations: bool,
    ReadPydanticModel: Type[BaseModel] | None = None,
    FullReadPydanticModel: Type[BaseModel] | None = None,
):
    if response_model_configs is None:
        response_model_configs = []
    final_routes_config: list[RouteConfig] = []
    for route_config in routes_config:
        response_model_config = next(
            (
                response_model_config
                for response_model_config in response_model_configs
                if response_model_config.route_name == route_config.route_name
            ),
            None,
        )
        route_config.extend_response_model(
            response_model_config=response_model_config,
            read_with_relations=read_with_relations,
            ReadPydanticModel=ReadPydanticModel,
            FullReadPydanticModel=FullReadPydanticModel,
        )
        final_routes_config.append(route_config)
    return final_routes_config


def format_init_data(
    init_data: list[RouteConfig],
    read_with_relations: bool,
    authorizations: list[AuthorizationConfig] | None = None,
    exclude_routes_name: list[DefaultRoutesName] | None = None,
    authentication: AuthenticationManager | None = None,
    response_model_configs: list[ResponseModelConfig] | None = None,
    roles: list[str] | None = None,
    privileges: list[str] | None = None,
    ReadPydanticModel: Type[BaseModel] | None = None,
    FullReadPydanticModel: Type[BaseModel] | None = None,
):
    formatted_data: list[RouteConfig] = []

    formatted_data = exclude_route(init_data, exclude_routes_name)
    formatted_data = (
        formatted_data
        if authorizations is None
        else add_authorizations(
            routes_config=formatted_data, authorizations=authorizations
        )
    )
    for route_config in formatted_data:
        if route_config.is_protected:
            route_config.dependencies = initialize_dependecies(
                config=route_config,
                authentication=authentication,
                roles=roles,
                privileges=privileges,
            )

    formatted_data = set_response_models(
        read_with_relations=read_with_relations,
        ReadPydanticModel=ReadPydanticModel,
        FullReadPydanticModel=FullReadPydanticModel,
        routes_config=formatted_data,
        response_model_configs=response_model_configs,
    )

    return formatted_data
