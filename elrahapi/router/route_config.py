from typing import Any, Callable
from elrahapi.router.router_routes_name import RoutesName,READ_ROUTES_NAME,DEFAULT_DETAIL_ROUTES_NAME
from elrahapi.router.route_additional_config import AuthorizationConfig, ResponseModelConfig
from elrahapi.authentication.authentication_manager import AuthenticationManager
class RouteConfig:

    def __init__(
        self,
        route_name: RoutesName,
        route_path: str | None = None,
        summary: str | None = None,
        description: str | None = None,
        is_activated: bool = False,
        is_protected: bool = False,
        roles: list[str] | None = None,
        privileges: list[str] | None = None,
        dependencies: list[Callable[..., Any] | None] = None,
        read_with_relations: bool | None = None,
        response_model: Any = None,
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

    @property
    def read_with_relations(self) -> bool:
        return self.__read_with_relations

    @read_with_relations.setter
    def read_with_relations(self, value: bool | None=None):
        if self.route_name not in READ_ROUTES_NAME and value is None:
            self.__read_with_relations =  False
        self.__read_with_relations= value

    def validate_route_path(
        self,
        route_name: RoutesName,
        route_path: str | None = None,
    ):
        if route_path:
            if route_name in DEFAULT_DETAIL_ROUTES_NAME and "{pk}" not in route_path:
                return f"/{route_name.value}/{{pk}}"
            return route_path
        else:
            return f"/{route_name.value}"

    def extend_response_model_config(self,response_model_config: ResponseModelConfig):
        if response_model_config.reponse_model:
            self.response_model = response_model_config.reponse_model
        if response_model_config.read_with_relations is not None:
            self.read_with_relations = response_model_config.read_with_relations

    def extend_authorization_config(self, authorization_config: AuthorizationConfig):
        if authorization_config.roles:
            self.roles.extend(authorization_config.roles)
        if authorization_config.privileges:
            self.privileges.extend(authorization_config.privileges)

    def get_authorizations(
        self, authentication: AuthenticationManager
    ) -> list[callable]:
        return authentication.check_authorizations(
                roles_name=self.roles, privileges_name=self.privileges
            )
