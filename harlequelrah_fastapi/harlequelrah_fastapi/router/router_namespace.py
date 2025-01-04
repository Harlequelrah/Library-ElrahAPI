from typing import List
from enum import Enum
from harlequelrah_fastapi.router.route_config import DEFAULT_ROUTE_CONFIG, RouteConfig
class DEFAULTROUTESNAME(str,Enum):
    COUNT='count'
    READ_ALL_BY_FILTER='read-all-by-filter'
    READ_ALL='read-all'
    READ_ONE='read-one'
    CREATE='create'
    UPDATE='update'
    DELETE='delete'
    READ_CURRENT_USER='read-current-user'
    TOKEN_URL='tokenUrl'
    GET_REFRESH_TOKEN='get-refresh-token'
    REFRESH_TOKEN='refresh-token'
    LOGIN='login'
    CHANGE_PASSWORD='change-password'


DEFAULT_ROUTES_CONFIGS: dict[str,DEFAULT_ROUTE_CONFIG] = {
    "count": DEFAULT_ROUTE_CONFIG(
        "Get count of entities", "Retrieve the total count of entities"
    ),
    "read-one":DEFAULT_ROUTE_CONFIG("Get one entity", "Retrieve one entity by id"),
    "read-all": DEFAULT_ROUTE_CONFIG( "Get all entities", "Retrieve all entities"),
    "read-all-by-filter":DEFAULT_ROUTE_CONFIG(
        "Get all entities by filter",
        "Retrieve entities by filter",
    ),
    "create":DEFAULT_ROUTE_CONFIG( "Create an entity", "Allow to create an entity"),
    "update":DEFAULT_ROUTE_CONFIG("Update an entity", "Allow to update an entity"),
    "delete":DEFAULT_ROUTE_CONFIG( "Delete an entity", "Allow to delete an entity"),
}

ROUTES_PUBLIC_CONFIG: List[RouteConfig] = [
    RouteConfig(
        route_name=route_name,
        is_activated=True,
        is_protected=False,
        summary=route_config.summary,
        description=route_config.description,
    )
    for route_name , route_config in DEFAULT_ROUTES_CONFIGS.items()
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
        description="retrieve one user from credential : id or email or username",
    ),
]
