from typing import Any, Callable, List, Optional, Type

from elrahapi.authentication.authentication_manager import AuthenticationManager
from elrahapi.router.router_routes_name import (
    DEFAULT_DETAIL_ROUTES_NAME,
    DefaultRoutesName,
    RelationRoutesName,
)
from pydantic import BaseModel


class DEFAULT_ROUTE_CONFIG:
    def __init__(self, summary: str, description: str):
        self.summary = summary
        self.description = description


class AuthorizationConfig:
    def __init__(
        self,
        route_name: DefaultRoutesName|RelationRoutesName,
        roles: Optional[List[str]] = None,
        privileges: Optional[List[str]] = None,
    ):
        self.route_name = route_name
        self.roles = roles if roles else []
        self.privileges = privileges if privileges else []


class ResponseModelConfig:

    def __init__(
        self,
        route_name: DefaultRoutesName | RelationRoutesName,
        read_with_relations: bool,
        reponse_model: Optional[Type[BaseModel]] = None,
    ):
        self.reponse_model = reponse_model
        self.route_name = route_name
        self.read_with_relations = read_with_relations


class RouteConfig:

    def __init__(
        self,
        route_name: DefaultRoutesName | RelationRoutesName,
        route_path: Optional[str] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        is_activated: bool = False,
        is_protected: bool = False,
        roles: Optional[List[str]] = None,
        privileges: Optional[List[str]] = None,
        dependencies: Optional[List[Callable[..., Any]]] = None,
        read_with_relations: Optional[bool] = None,
        response_model: Optional[Any] = None,
    ):
        self.route_name = route_name
        self.is_activated = is_activated
        self.is_protected = is_protected
        self.route_path = self.validate_route_path(route_name, route_path)
        self.summary = summary
        self.description = description
        self.response_model = response_model
        self.dependencies = dependencies if dependencies else []
        self.read_with_relations = read_with_relations
        self.roles = [role.strip().upper() for role in roles if roles] if roles else []
        self.privileges = (
            [auth.strip().upper() for auth in privileges] if privileges else []
        )

    def validate_route_path(
        self,
        route_name: DefaultRoutesName | RelationRoutesName,
        route_path: Optional[str] = None,
    ):
        if route_path:
            # print(f"route_name : {route_name} route_path : {route_path}")
            if route_name in DEFAULT_DETAIL_ROUTES_NAME and "{pk}" not in route_path:
                return f"/{route_name.value}/{{pk}}"
            return route_path
        else:
            return f"/{route_name.value}"
            # print(f"route_name : {route_name} route_path : {route_path}")
            # if route_name  in DEFAULT_NO_DETAIL_ROUTES_NAME:
            #     return ""

    def extend_authorization_config(self, authorization_config: AuthorizationConfig):
        if authorization_config.roles:
            self.roles.extend(authorization_config.roles)
        if authorization_config.privileges:
            self.privileges.extend(authorization_config.privileges)

    def get_authorizations(
        self, authentication: AuthenticationManager
    ) -> List[callable]:
        return authentication.check_authorizations(
            roles_name=self.roles, privileges_name=self.privileges
        )
