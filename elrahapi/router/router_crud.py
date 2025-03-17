from typing import List, Optional

from fastapi import Depends
from elrahapi.authentication.authentication_manager import AuthenticationManager
from elrahapi.router.route_config import (
    DEFAULT_ROUTE_CONFIG,
    AuthorizationConfig,
    RouteConfig,
)
from elrahapi.router.router_namespace import (
    DEFAULT_ROUTES_CONFIGS,
    DefaultRoutesName,
    USER_AUTH_CONFIG,
    TypeRoute,
)


def exclude_route(
    routes: List[RouteConfig],
    exclude_routes_name: Optional[List[DefaultRoutesName]] = None,
):
    init_data: List[RouteConfig] = []
    if exclude_routes_name:
        for route in routes:
            if route.route_name not in [
                route_name for route_name in exclude_routes_name
            ]:
                init_data.append(route)
    return init_data if init_data else routes


def get_single_route(
    route_name: DefaultRoutesName, type_route: Optional[TypeRoute] = TypeRoute.PUBLIC
) -> RouteConfig:
    config: DEFAULT_ROUTE_CONFIG = DEFAULT_ROUTES_CONFIGS.get(route_name)
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
    authentication: Optional[AuthenticationManager]=None,
    roles: Optional[List[str]] = None,
    privileges: Optional[List[str]] = None,
):
    if not authentication : return []
    dependencies = []
    if config.is_protected:
        if roles:
            for role in roles:
                config.roles.append(role)
        if privileges:
            for privilege in privileges:
                config.privileges.append(privilege)
        if config.roles or config.privileges:
            authorizations: List[callable] = config.get_authorizations(
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
    authorized_routes_config:List[RouteConfig] = []
    for route_config in routes_config:
        authorization = next(
            (
                authorization
                for authorization in authorizations
                if authorization.route_name == route_config.route_name
            ),
            None,
        )
        route_config.roles.extend(authorization.roles)
        route_config.privileges.extend(authorization.privileges)
        authorized_routes_config.append(route_config)
    return authorized_routes_config


def format_init_data(
    init_data: List[RouteConfig],
    authorizations: Optional[List[AuthorizationConfig]] = None,
    exclude_routes_name: Optional[List[DefaultRoutesName]] = None,
):
    init_data = exclude_route(init_data, exclude_routes_name)
    init_data = (
        init_data
        if authorizations is None
        else add_authorizations(init_data, authorizations)
    )
    return init_data


