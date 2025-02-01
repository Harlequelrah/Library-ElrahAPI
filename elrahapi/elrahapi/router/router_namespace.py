from typing import List
from enum import Enum

from elrahapi.router.router_default_routes_name import DefaultRoutesName
from .route_config import DEFAULT_ROUTE_CONFIG, RouteConfig





class TypeRoute(str, Enum):
    PUBLIC = "public"
    PROTECTED = "protected"


DEFAULT_ROUTES_CONFIGS: dict[DefaultRoutesName, DEFAULT_ROUTE_CONFIG] = {
    DefaultRoutesName.COUNT: DEFAULT_ROUTE_CONFIG(
        "Get count of entities", "Retrieve the total count of entities"
    ),
    DefaultRoutesName.READ_ONE: DEFAULT_ROUTE_CONFIG(
        "Get one entity", "Retrieve one entity by id"
    ),
    DefaultRoutesName.READ_ALL: DEFAULT_ROUTE_CONFIG(
        "Get all entities", "Retrieve all entities"
    ),
    DefaultRoutesName.READ_ALL_BY_FILTER: DEFAULT_ROUTE_CONFIG(
        "Get all entities by filter",
        "Retrieve entities by filter",
    ),
    DefaultRoutesName.CREATE: DEFAULT_ROUTE_CONFIG(
        "Create an entity", "Allow to create an entity"
    ),
    DefaultRoutesName.UPDATE: DEFAULT_ROUTE_CONFIG(
        "Update an entity", "Allow to update an entity"
    ),
    DefaultRoutesName.DELETE: DEFAULT_ROUTE_CONFIG(
        "Delete an entity", "Allow to delete an entity"
    ),
}

ROUTES_PUBLIC_CONFIG: List[RouteConfig] = [
    RouteConfig(
        route_name=route_name,
        is_activated=True,
        is_protected=False,
        summary=route_config.summary,
        description=route_config.description,
    )
    for route_name, route_config in DEFAULT_ROUTES_CONFIGS.items()
]
ROUTES_PROTECTED_CONFIG: List[RouteConfig] = [
    RouteConfig(
        route_name=route_name,
        is_activated=True,
        is_protected=True,
        summary=route_config.summary,
        description=route_config.description,
    )
    for route_name, route_config in DEFAULT_ROUTES_CONFIGS.items()
]
USER_AUTH_CONFIG: dict[DefaultRoutesName, RouteConfig] = {
    DefaultRoutesName.READ_CURRENT_USER: RouteConfig(
        route_name="read-current-user",
        is_activated=True,
        is_protected=True,
        summary="read current user",
        description=" read current user informations",
    ),
    DefaultRoutesName.TOKEN_URL: RouteConfig(
        route_name="tokenUrl",
        is_activated=True,
        summary="Swagger UI's scopes",
        description="provide scopes for Swagger UI operations",
    ),
    DefaultRoutesName.GET_REFRESH_TOKEN: RouteConfig(
        route_name="get-refresh-token",
        is_activated=True,
        is_protected=True,
        summary="get refresh token",
        description="allow you to retrieve refresh token",
    ),
    DefaultRoutesName.REFRESH_TOKEN: RouteConfig(
        route_name="refresh-token",
        is_activated=True,
        summary="refresh token",
        description="refresh your access token with refresh token",
    ),
    DefaultRoutesName.LOGIN: RouteConfig(
        route_name="login",
        is_activated=True,
        summary="login",
        description="allow you to login",
    ),
    DefaultRoutesName.CHANGE_PASSWORD: RouteConfig(
        route_name="change-password",
        is_activated=True,
        is_protected=True,
        summary="change password",
        description="allow you to change your password",
    ),
    DefaultRoutesName.READ_ONE_USER: RouteConfig(
        route_name="read-one-user",
        route_path="/read-one-user/{username_or_email}",
        is_activated=True,
        is_protected=True,
        summary="read one user ",
        description="retrieve one user from credential :  email or username",
    ),
}
USER_AUTH_CONFIG_ROUTES: List[RouteConfig] = [
    route for route in USER_AUTH_CONFIG.values()
]
