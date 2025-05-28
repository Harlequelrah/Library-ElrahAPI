from pydantic import BaseModel
from typing import  List, Optional, Type
from elrahapi.router.router_routes_name import RoutesName

class DefaultRouteConfig:
    def __init__(self, summary: str, description: str):
        self.summary = summary
        self.description = description


class ResponseModelConfig:

    def __init__(
        self,
        route_name: RoutesName,
        read_with_relations: Optional[bool]=None,
        reponse_model: Optional[Type[BaseModel]] = None,
    ):
        self.reponse_model = reponse_model
        self.route_name = route_name
        self.read_with_relations = read_with_relations


class AuthorizationConfig:
    def __init__(
        self,
        route_name: RoutesName,
        roles: Optional[List[str]] = None,
        privileges: Optional[List[str]] = None,
    ):
        self.route_name = route_name
        self.roles = roles if roles else []
        self.privileges = privileges if privileges else []
