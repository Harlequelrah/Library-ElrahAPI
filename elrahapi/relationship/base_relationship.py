from abc import ABC

from elrahapi.authentication.authentication_manager import AuthenticationManager
from elrahapi.crud.crud_forgery import CrudForgery
from elrahapi.router.route_additional_config import (
    AuthorizationConfig,
    ResponseModelConfig,
)
from elrahapi.router.route_config import RouteConfig
from elrahapi.router.router_crud import (
    add_authorizations,
    initialize_dependecies,
    set_response_models,
)
from elrahapi.router.router_routes_name import RelationRoutesName


class BaseRelationship(ABC):
    RELATION_RULES = []

    def __init__(
        self,
        relationship_name: str,
        second_entity_crud: CrudForgery,
        relations_routes_configs: list[RouteConfig] | None = None,
        relations_authorizations_configs: AuthorizationConfig | None = None,
        relations_responses_model_configs: ResponseModelConfig | None = None,
        default_public_relation_routes_name: list[RelationRoutesName] | None = None,
        default_protected_relation_routes_name: list[RelationRoutesName] | None = None,
    ):
        self.relationship_name = relationship_name
        self.relationship_name = relationship_name
        self.second_entity_crud = second_entity_crud
        self.relations_routes_configs = relations_routes_configs or []
        self.default_public_relation_routes_name = (
            default_public_relation_routes_name or []
        )
        self.default_protected_relation_routes_name = (
            default_protected_relation_routes_name or []
        )
        self.relations_authorizations_configs = relations_authorizations_configs or []
        self.relations_responses_model_configs = relations_responses_model_configs or []
        self.yield_session = second_entity_crud.session_manager.yield_session

    def get_second_model_key(self):
        return self.second_entity_crud.crud_models.get_pk()

    def is_verified_relation_rule(
        self,
        relation_route_name: RelationRoutesName,
    ):
        return relation_route_name in self.RELATION_RULES

    def check_relation_rules(self):
        for route_config in self.relations_routes_configs:
            if not self.is_verified_relation_rule(
                relation_route_name=route_config.route_name,
            ):
                raise ValueError(
                    f" Route operation {route_config.route_name} not allowed for the relation type {self.type_relation}"
                )

    def init_default_routes(
        self,
    ):
        self.check_relation_rules()
        all_routes_configs = (
            self.default_public_relation_routes_name
            + self.default_protected_relation_routes_name
        )
        routes_configs: list[RouteConfig] = []
        second_entity_name = self.second_entity_crud.entity_name
        path = f"/{{pk1}}/{second_entity_name}"
        for route_name in all_routes_configs:
            if route_name == RelationRoutesName.READ_ALL_BY_RELATION:
                route_config = RouteConfig(
                    route_name=route_name,
                    route_path=path + "s",
                    summary=f"Retrive {self.relationship_name}",
                    description=f"Allow to retrive all {second_entity_name}s from the relation",
                    is_activated=True,
                    response_model=self.second_entity_crud.crud_models.read_model,
                    is_protected=(
                        False
                        if route_name in self.default_public_relation_routes_name
                        else True
                    ),
                )
                routes_configs.append(route_config)
            if route_name == RelationRoutesName.READ_ONE_BY_RELATION:
                route_config = RouteConfig(
                    route_name=route_name,
                    route_path=path,
                    summary=f"Retrive one of {self.relationship_name}",
                    description=f"Allow to retrive  one {second_entity_name} from the relation",
                    is_activated=True,
                    response_model=self.second_entity_crud.crud_models.read_model,
                    is_protected=(
                        False
                        if route_name in self.default_public_relation_routes_name
                        else True
                    ),
                )
                routes_configs.append(route_config)

            if route_name == RelationRoutesName.CREATE_RELATION:
                route_config = RouteConfig(
                    route_name=route_name,
                    route_path=path + f"s/{{pk2}}",
                    summary=f"Create one {self.relationship_name} relation",
                    description=f"Allow to link with {second_entity_name}",
                    is_activated=True,
                    is_protected=(
                        True
                        if route_name in self.default_protected_relation_routes_name
                        else False
                    ),
                )
                routes_configs.append(route_config)
            if route_name == RelationRoutesName.DELETE_RELATION:
                route_config = RouteConfig(
                    route_name=route_name,
                    route_path=path + f"s/{{pk2}}",
                    summary=f"delete one {self.relationship_name} relation",
                    description=f"Allow to unlink with {second_entity_name}",
                    is_activated=True,
                    is_protected=(
                        True
                        if route_name in self.default_protected_relation_routes_name
                        else False
                    ),
                )
                routes_configs.append(route_config)

            if route_name == RelationRoutesName.DELETE_BY_RELATION:
                route_config = RouteConfig(
                    route_name=route_name,
                    route_path=path,
                    summary=f"Delete {self.relationship_name}",
                    description=f"Allow to delete {second_entity_name} by the relation",
                    is_activated=True,
                    is_protected=(
                        True
                        if route_name in self.default_protected_relation_routes_name
                        else False
                    ),
                )
                routes_configs.append(route_config)
            if route_name == RelationRoutesName.SOFT_DELETE_BY_RELATION:
                route_config = RouteConfig(
                    route_name=route_name,
                    route_path=path + "/soft-delete",
                    summary=f"Soft Delete {self.relationship_name}",
                    description=f"Allow to soft delete {second_entity_name} by the relation",
                    is_activated=True,
                    is_protected=(
                        True
                        if route_name in self.default_protected_relation_routes_name
                        else False
                    ),
                )
                routes_configs.append(route_config)
            if route_name == RelationRoutesName.CREATE_BY_RELATION:
                route_config = RouteConfig(
                    route_name=route_name,
                    route_path=path,
                    summary=f"Create {self.relationship_name}",
                    description=f"Allow to create {second_entity_name} by the relation",
                    is_activated=True,
                    is_protected=(
                        True
                        if route_name in self.default_protected_relation_routes_name
                        else False
                    ),
                    response_model=self.second_entity_crud.crud_models.read_model,
                )
                routes_configs.append(route_config)

            if route_name == RelationRoutesName.UPDATE_BY_RELATION:
                route_config = RouteConfig(
                    route_name=route_name,
                    route_path=path,
                    summary=f"Update {self.relationship_name}",
                    description=f"Allow to update {second_entity_name} by the relation",
                    is_activated=True,
                    is_protected=(
                        True
                        if route_name in self.default_protected_relation_routes_name
                        else False
                    ),
                    response_model=self.second_entity_crud.crud_models.read_model,
                )
                routes_configs.append(route_config)

            if route_name == RelationRoutesName.PATCH_BY_RELATION:
                route_config = RouteConfig(
                    route_name=route_name,
                    route_path=path,
                    summary=f"Patch {self.relationship_name}",
                    description=f"Allow to patch {second_entity_name} by the relation",
                    is_activated=True,
                    is_protected=(
                        True
                        if route_name in self.default_protected_relation_routes_name
                        else False
                    ),
                    response_model=self.second_entity_crud.crud_models.read_model,
                )
                routes_configs.append(route_config)

        return routes_configs

    def purge_relations(self, routes_configs: list[RouteConfig]):
        purged_routes_configs: list[RouteConfig] = []
        for route_config in routes_configs:
            if (
                self.is_verified_relation_rule(
                    relation_route_name=route_config.route_name,
                )
                and route_config.is_activated
            ):
                purged_routes_configs.append(route_config)
        return purged_routes_configs

    def init_routes_configs(
        self,
        authentication: AuthenticationManager | None = None,
        roles: list[str] | None = None,
        privileges: list[str] | None = None,
    ):
        routes_configs = self.init_default_routes() + self.relations_routes_configs
        purged_routes_configs = self.purge_relations(routes_configs)
        purged_routes_configs = (
            add_authorizations(
                routes_configs=purged_routes_configs,
                authorizations=self.relations_authorizations_configs,
            )
            if self.relations_authorizations_configs
            else purged_routes_configs
        )
        purged_routes_configs = (
            set_response_models(
                routes_config=purged_routes_configs,
                response_model_configs=self.relations_responses_model_configs,
            )
            if self.relations_responses_model_configs
            else purged_routes_configs
        )
        return self.initialize_relation_route_configs_dependencies(
            routes_configs=purged_routes_configs,
            authentication=authentication,
            roles=roles,
            privileges=privileges,
        )

    def initialize_relation_route_configs_dependencies(
        self,
        routes_configs: list[RouteConfig],
        authentication: AuthenticationManager | None = None,
        roles: list[str] | None = None,
        privileges: list[str] | None = None,
    ) -> list[RouteConfig]:
        if not authentication:
            routes_configs
        for route_config in routes_configs:
            if route_config.is_protected:
                route_config.dependencies = initialize_dependecies(
                    config=route_config,
                    authentication=authentication,
                    roles=roles,
                    privileges=privileges,
                )
        return routes_configs
