from typing import  List, Optional, Type
from elrahapi.authentication.authentication_manager import AuthenticationManager
from elrahapi.router.route_config import (
    AuthorizationConfig,
    ResponseModelConfig,
    RouteConfig,
)
from elrahapi.router.router_namespace import (
    DEFAULT_ROUTES_CONFIGS,
    RELATION_RULES,
    USER_AUTH_CONFIG,
    TypeRelation,
    TypeRoute,
    DefaultRouteConfig
)
from pydantic import BaseModel
from fastapi import Depends
from elrahapi.router.router_routes_name import RelationRoutesName, DefaultRoutesName,RoutesName


def exclude_route(
    routes: List[RouteConfig],
    exclude_routes_name: Optional[List[RoutesName]] = None,
):
    init_data: List[RouteConfig] = []
    if exclude_routes_name:
        for route in routes:
            if route.route_name not in exclude_routes_name and route.is_activated:
                init_data.append(route)
    return init_data if init_data else routes


def get_single_route(
    route_name: DefaultRoutesName, type_route: Optional[TypeRoute] = TypeRoute.PUBLIC
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
    authentication: Optional[AuthenticationManager] = None,
    roles: Optional[List[str]] = None,
    privileges: Optional[List[str]] = None,
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
            authorizations: List[callable] =  config.get_authorizations(
                authentication=authentication
            )
            dependencies: List[Depends] = [
                Depends(authorization) for authorization in authorizations
            ]
        else:
            dependencies = [Depends(authentication.get_access_token)]
    return dependencies


def add_authorizations(
    routes_config: List[RouteConfig], authorizations: List[AuthorizationConfig]
):
    authorized_routes_config: List[RouteConfig] = []
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


def set_response_model_config(
    routes_config: List[RouteConfig],
    response_model_configs: List[ResponseModelConfig],
):
    final_routes_config: List[RouteConfig] = []
    for route_config in routes_config:
        response_model_config = next(
            (
                response_model_config
                for response_model_config in response_model_configs
                if response_model_config.route_name == route_config.route_name
            ),
            None,
        )
        if response_model_config:
            route_config.extend_response_model_config(response_model_config=response_model_config)
            final_routes_config.append(route_config)
    return final_routes_config


def format_init_data(
    init_data: List[RouteConfig],
    read_with_relations: bool,
    authorizations: Optional[List[AuthorizationConfig]] = None,
    exclude_routes_name: Optional[List[DefaultRoutesName]] = None,
    authentication: Optional[AuthenticationManager] = None,
    response_model_configs: Optional[List[ResponseModelConfig]] = None,
    roles: Optional[List[str]] = None,
    privileges: Optional[List[str]] = None,
    ReadPydanticModel: Optional[Type[BaseModel]] = None,
    FullReadPydanticModel: Optional[Type[BaseModel]] = None,
):
    formatted_data: List[RouteConfig] = []

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
            route_config.dependencies =  initialize_dependecies(
                config=route_config,
                authentication=authentication,
                roles=roles,
                privileges=privileges,
            )

    formatted_data = (
        formatted_data
        if response_model_configs is None
        else set_response_model_config(
            routes_config=formatted_data, response_model_configs=response_model_configs
        )
    )
    for route_config in formatted_data:
        response_model = set_response_model(
                route_config=route_config,
                read_with_relations=read_with_relations,
                ReadPydanticModel=ReadPydanticModel,
                FullReadPydanticModel=FullReadPydanticModel,
            )
        route_config.response_model = response_model
    return formatted_data


def set_response_model(
    route_config: RouteConfig,
    read_with_relations: bool,
    ReadPydanticModel: Optional[Type[BaseModel]] = None,
    FullReadPydanticModel: Optional[Type[BaseModel]] = None,
):
    if FullReadPydanticModel is None:
        return ReadPydanticModel
    if route_config.read_with_relations:
        return FullReadPydanticModel
    else:
        if route_config.read_with_relations is False:
            return ReadPydanticModel
        elif route_config.read_with_relations is None:
            if read_with_relations:
                return FullReadPydanticModel
            else:
                return ReadPydanticModel


def is_verified_relation_rule(
    type_relation: TypeRelation,
    relation_route_name: RelationRoutesName,
):
    return relation_route_name in RELATION_RULES[type_relation]



