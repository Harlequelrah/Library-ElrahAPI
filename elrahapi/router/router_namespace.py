from enum import Enum

from elrahapi.router.route_additional_config import DefaultRouteConfig
from elrahapi.router.route_config import RouteConfig
from elrahapi.router.router_routes_name import DefaultRoutesName, RelationRoutesName


class TypeRoute(str, Enum):
    PUBLIC = "PUBLIC"
    PROTECTED = "PROTECTED"


class TypeRelation(str, Enum):
    ONE_TO_ONE = "One To One"
    ONE_TO_MANY = "One To Many"
    MANY_TO_MANY_CLASS = "Many To Many Class"
    MANY_TO_MANY_TABLE = "Many To Many Table"
    MANY_TO_ONE = "Many To One"


DEFAULT_ROUTES_CONFIGS: dict[DefaultRoutesName, DefaultRouteConfig] = {
    DefaultRoutesName.COUNT: DefaultRouteConfig(
        "Get count of entities", "Retrieve the total count of entities"
    ),
    DefaultRoutesName.READ_ALL: DefaultRouteConfig(
        "Get all entities", "Retrieve all entities"
    ),
    DefaultRoutesName.READ_ONE: DefaultRouteConfig(
        "Get one entity", "Retrieve one entity by id"
    ),
    DefaultRoutesName.BULK_CREATE: DefaultRouteConfig(
        "Create entities", "Allow to create many entities"
    ),
    DefaultRoutesName.BULK_DELETE: DefaultRouteConfig(
        "Delete entities", "Allow to delete many entities"
    ),
    DefaultRoutesName.UPDATE: DefaultRouteConfig(
        "Update an entity", "Allow to update an entity"
    ),
    DefaultRoutesName.PATCH: DefaultRouteConfig(
        "Patch an entity", "Allow to patch an entity"
    ),
    DefaultRoutesName.CREATE: DefaultRouteConfig(
        "Create an entity", "Allow to create an entity"
    ),
    DefaultRoutesName.DELETE: DefaultRouteConfig(
        "Delete an entity", "Allow to delete an entity"
    ),
    DefaultRoutesName.SOFT_DELETE: DefaultRouteConfig(
        "Soft delete an entity", "Allow to soft delete an entity"
    ),
    DefaultRoutesName.BULK_SOFT_DELETE: DefaultRouteConfig(
        "Bulk soft delete an entity", "Allow to bulk soft delete many entities"
    ),
}


ROUTES_PUBLIC_CONFIG: list[RouteConfig] = [
    RouteConfig(
        route_name=route_name,
        is_activated=True,
        is_protected=False,
        summary=route_config.summary,
        description=route_config.description,
    )
    for route_name, route_config in DEFAULT_ROUTES_CONFIGS.items()
]
ROUTES_PROTECTED_CONFIG: list[RouteConfig] = [
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
        route_name=DefaultRoutesName.READ_CURRENT_USER,
        route_path="/read-current-user",
        is_activated=True,
        is_protected=True,
        summary="read current user",
        description=" read current user informations",
    ),
    DefaultRoutesName.TOKEN_URL: RouteConfig(
        route_name=DefaultRoutesName.TOKEN_URL,
        is_activated=True,
        summary="Swagger UI's scopes",
        description="provide scopes for Swagger UI operations",
    ),
    # DefaultRoutesName.GET_REFRESH_TOKEN: RouteConfig(
    #     route_name=DefaultRoutesName.GET_REFRESH_TOKEN,
    #     is_activated=True,
    #     is_protected=True,
    #     summary="get refresh token",
    #     description="allow you to retrieve refresh token",
    # ),
    DefaultRoutesName.REFRESH_TOKEN: RouteConfig(
        route_name=DefaultRoutesName.REFRESH_TOKEN,
        is_activated=True,
        # is_protected=True,
        summary="refresh token",
        description="refresh your access token with refresh token",
    ),
    DefaultRoutesName.LOGIN: RouteConfig(
        route_name=DefaultRoutesName.LOGIN,
        is_activated=True,
        summary="login",
        description="allow you to login",
    ),
    DefaultRoutesName.CHANGE_PASSWORD: RouteConfig(
        route_name=DefaultRoutesName.CHANGE_PASSWORD,
        is_activated=True,
        is_protected=True,
        summary="change password",
        description="allow you to change your password",
    ),
    DefaultRoutesName.READ_ONE_USER: RouteConfig(
        route_name=DefaultRoutesName.READ_ONE_USER,
        route_path="/read-one-user/{sub}",
        is_activated=True,
        is_protected=True,
        summary="read one user ",
        description="retrieve one user from sub :  email or username or pk",
    ),
    DefaultRoutesName.CHANGE_USER_STATE: RouteConfig(
        route_name=DefaultRoutesName.CHANGE_USER_STATE,
        route_path="/change-user-state/{pk}",
        is_activated=True,
        is_protected=True,
        summary="change user state ",
        description="change user state (active or inactive)",
    ),
}
USER_AUTH_CONFIG_ROUTES: list[RouteConfig] = [
    route for route in USER_AUTH_CONFIG.values()
]
