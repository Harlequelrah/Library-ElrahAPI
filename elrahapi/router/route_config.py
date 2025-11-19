from typing import Any, Callable, Type

from elrahapi.authentication.authentication_manager import AuthenticationManager
from elrahapi.router.route_additional_config import (
    AuthorizationConfig,
    ResponseModelConfig,
)
from elrahapi.router.router_routes_name import (
    DEFAULT_DETAIL_ROUTES_NAME,
    DEFAULT_ROUTES_NAME,
    READ_ROUTES_NAME,
    DefaultRoutesName,
    RoutesName,
)
from pydantic import BaseModel


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
    def read_with_relations(self, value: bool | None = None):
        if self.route_name not in READ_ROUTES_NAME and value is None:
            self.__read_with_relations = False
        self.__read_with_relations = value

    def validate_route_path(
        self,
        route_name: RoutesName,
        route_path: str | None = None,
    ):
        if route_path:
            return route_path
        if route_name in DEFAULT_ROUTES_NAME:
            if route_name in DEFAULT_DETAIL_ROUTES_NAME:
                return f"/{{pk}}"
            else:
                return ""
        elif route_name == DefaultRoutesName.CHANGE_USER_STATE:
            print("here")
            return f"/change-user-state/{{pk}}"
        else:
            if route_name == DefaultRoutesName.SOFT_DELETE:
                return f"/soft-delete/{{pk}}"
            elif route_name in [
                DefaultRoutesName.BULK_CREATE,
                DefaultRoutesName.BULK_DELETE,
            ]:
                return f"/bulk"
            elif route_name == DefaultRoutesName.BULK_SOFT_DELETE:
                return f"/bulk/soft-delete"
        return f"/{route_name.value}"

    def extend_response_model(
        self,
        response_model_config: ResponseModelConfig | None,
        read_with_relations: bool,
        ReadPydanticModel: Type[BaseModel] | None = None,
        FullReadPydanticModel: Type[BaseModel] | None = None,
    ):
        response_model: Type[BaseModel] | None = None
        if response_model_config is None:
            if self.response_model is None:
                if self.read_with_relations:
                    response_model = FullReadPydanticModel
                else:
                    if read_with_relations:
                        response_model = FullReadPydanticModel
                    else:
                        response_model = ReadPydanticModel
        else:
            self.read_with_relations = response_model_config.read_with_relations
            if response_model_config.response_model:
                self.response_model = response_model_config.response_model
            else:
                if FullReadPydanticModel is None:
                    self.response_model = ReadPydanticModel
                else:
                    self.read_with_relations = (
                        self.read_with_relations
                        if self.read_with_relations is not None
                        else read_with_relations
                    )
                    if self.read_with_relations:
                        response_model = FullReadPydanticModel
                    else:
                        response_model = ReadPydanticModel
        self.response_model = response_model

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
