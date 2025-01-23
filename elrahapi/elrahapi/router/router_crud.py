from typing import List, Optional

from fastapi import Depends
from elrahapi.authentication.authenticate import Authentication
from elrahapi.router.route_config import DEFAULT_ROUTE_CONFIG, RouteConfig
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
                route_name.value for route_name in exclude_routes_name
            ]:
                init_data.append(route)
    return init_data if init_data else routes


def get_single_route(
    route_name: DefaultRoutesName, type_route: Optional[TypeRoute] = TypeRoute.PUBLIC
) -> RouteConfig:
    config: DEFAULT_ROUTE_CONFIG = DEFAULT_ROUTES_CONFIGS.get(route_name)
    if config:
        return RouteConfig(
            route_name=route_name.value,
            is_activated=True,
            summary=config.summary,
            description=config.description,
            is_protected=type_route == TypeRoute.PROTECTED,
        )
    else:
        return USER_AUTH_CONFIG[route_name]


def initialize_dependecies(
    config: RouteConfig,
    authentication: Authentication,
    roles: Optional[List[str]],
    privileges: Optional[List[str]],
):
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
