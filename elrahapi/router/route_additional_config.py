from pydantic import BaseModel
from typing import Type
from elrahapi.router.router_routes_name import RoutesName


class DefaultRouteConfig:
    def __init__(self, summary: str, description: str):
        self.summary = summary
        self.description = description


class ResponseModelConfig:

    def __init__(
        self,
        route_name: RoutesName,
        read_with_relations: bool | None = None,
        response_model: Type[BaseModel] | None = None,
    ):
        self.response_model = response_model
        self.route_name = route_name
        self.read_with_relations = read_with_relations


class AuthorizationConfig:
    def __init__(
        self,
        route_name: RoutesName,
        roles: list[str] | None = None,
        privileges: list[str] | None = None,
    ):
        self.route_name = route_name
        self.roles = roles if roles else []
        self.privileges = privileges if privileges else []
