from typing import List, Type,Optional
from copy import deepcopy
from elrahapi.crud.crud_models import CrudModels
from elrahapi.router.route_config import RouteConfig,ResponseModelConfig,AuthorizationConfig
from elrahapi.router.router_routes_name import DefaultRoutesName,RelationRoutesName
from elrahapi.router.router_namespace import  TypeRelation, TypeRoute
from elrahapi.authentication.authentication_manager import AuthenticationManager
from elrahapi.router.router_crud import initialize_dependecies, verify_relation_rule


class RelationRouteConfig:
    def __init__(
        self,
        route_config:Optional[RouteConfig]=None,
        type_route:Optional[TypeRoute]=None,
        response_model_config:Optional[ResponseModelConfig]=None,
        authorization_config:Optional[AuthorizationConfig]=None):
        self.response_model_config=response_model_config
        self.authorization_config=authorization_config
        self.type_route=type_route
        self.route_config=self.init_config() if route_config else route_config

    def init_config(self)->RouteConfig:
        if self.route_config:
            if (
                not self.route_config.is_protected,
                self.type_route and
                self.type_route == TypeRoute.PROTECTED
            ):
                self.route_config.is_protected=True
            if self.response_model_config and not self.route_config.response_model:
                self.route_config.response_model = self.response_model_config.reponse_model

            if self.authorization_config :
                self.route_config.extend_authorization_config(
                    authorization_config=self.authorization_config)
        return self.route_config


class Relationship:



    def __init__(
        self,
        relationship_name: str,
        second_model_key_name: str,
        second_entity_crud_models: CrudModels,
        type_relation:TypeRelation,
        relationship_crud_models: Optional[CrudModels] = None,
        relationship_key1_name: Optional[str] = None,
        relationship_key2_name: Optional[str] = None,
        relations_routes_configs:Optional[RouteConfig]=None,
        relations_authorizations_configs:Optional[AuthorizationConfig]=None,
        relations_responses_model_configs:Optional[ResponseModelConfig]=None,
        default_public_relation_routes_name : List[RelationRoutesName]=None,
        default_protected_relation_routes_name:List[RelationRoutesName]=None,
    ):
        if type_relation == TypeRelation.MANY_TO_MANY_CLASS:
            self.check_many_to_many_class_attrs(
                relationship_crud_models=relationship_crud_models,
                relationship_key1_name=relationship_key1_name,
                relationship_key2_name=relationship_key2_name
            )
        self.relationship_name = relationship_name
        self.relationship_crud_models = relationship_crud_models
        self.second_entity_crud_models = second_entity_crud_models
        self.relationship_key1_name = relationship_key1_name
        self.relationship_key2_name = relationship_key2_name
        self.second_model_key_name = second_model_key_name
        self.type_relation=type_relation
        self.relations_routes_configs=self.init_routes_configs(
            default_public_relation_routes_name=default_public_relation_routes_name,
            default_protected_relation_routes_name=default_protected_relation_routes_name,
            relations_routes_configs=relations_routes_configs,
            relations_authorizations_configs=relations_authorizations_configs,
            relations_responses_model_configs=relations_responses_model_configs
            ) if relations_routes_configs else []

    def init_default_routes(
        self,
        default_public_relation_routes_name : List[RelationRoutesName]=None,
        default_protected_relation_routes_name:List[RelationRoutesName]=None,
    ):
        routes_configs:List[RouteConfig]=[]
        second_entity_name=self.second_entity_crud_models.entity_name
        path = f"/{{pk1}}/{second_entity_name}"
        for route_name in default_public_relation_routes_name+default_protected_relation_routes_name:
            if route_name==RelationRoutesName.READ_ALL_RELATION:
                route_config = RouteConfig(
                    route_name=DefaultRoutesName.READ_ALL_RELATION,
                    route_path=path+"s",
                    summary=f"Retrive all {second_entity_name}s",
                    description=f"Allow to retrive all {second_entity_name}s from the relation",
                    is_activated=True,
                    response_model=self.second_entity_crud_models.read_model,
                )
                routes_configs.append(route_config)
            if route_name == RelationRoutesName.READ_ONE_RELATION:
                route_config = RouteConfig(
                    route_name=DefaultRoutesName.READ_ONE_RELATION,
                    route_path=path+f"s",
                    summary=f"Retrive all {second_entity_name}s",
                    description=f"Allow to retrive all {second_entity_name}s from the relation",
                    is_activated=True,
                    response_model=self.second_entity_crud_models.read_model,
                )
                routes_configs.append(route_config)

    def purge_relations(self,routes_configs:List[RouteConfig]):
        purged_routes_configs:List[RouteConfig]=[]
        for route_config in routes_configs:
            if  verify_relation_rule(
                type_relation=self.type_relation,
                relation_route_name=route_config.route_name
            ) and route_config.is_activated:
                purged_routes_configs.append(route_config)
        return purged_routes_configs

    def init_routes_configs(
        self,
        relations_routes_configs: Optional[RouteConfig] = None,
        relations_authorizations_configs: Optional[AuthorizationConfig] = None,
        relations_responses_model_configs: Optional[ResponseModelConfig] = None,
        default_public_relation_routes_name: List[RelationRoutesName] = None,
        default_protected_relation_routes_name: List[RelationRoutesName] = None,
    ):
        routes_configs:List[RouteConfig]=[]
        if default_protected_relation_routes_name or default_public_relation_routes_name:
            default_routes_configs=self.init_default_routes(
                default_public_relation_routes_name=default_public_relation_routes_name,
                default_protected_relation_routes_name=default_protected_relation_routes_name,
            )
            if relations_routes_configs is None :
                routes_configs=default_routes_configs
            else :
                routes_configs= deepcopy(relations_routes_configs)+default_routes_configs

        purged_routes_configs= self.purge_relations(routes_configs)

        if read_all_relations_route_config:
            r1=read_all_relations_route_config
        else :
            route_config=RouteConfig(

            )
            r1=RelationRouteConfig(
                route_config=route_config,
                type_route=type_routes
            )
        if create_relation_route_config:
            r2 = create_relation_route_config
        else:
            route_config = RouteConfig(
                route_name=DefaultRoutesName.CREATE_RELATION,
                route_path=route_path,
                summary=f"Create one {rel_entity_name}",
                description=f"Allow to create {rel_entity_name}s to the relation",
                is_activated=True,
            )
            r2 = RelationRouteConfig(route_config=route_config, type_route=type_routes)

        if delete_relation_route_config:
            r3 = delete_relation_route_config
        else:
            route_config = RouteConfig(
                route_name=DefaultRoutesName.DELETE_RELATION,
                route_path=route_path,
                summary=f"Delete one {rel_entity_name}",
                description=f"Allow to delete {rel_entity_name}s from the relation",
                is_activated=True,
            )
            r3 = RelationRouteConfig(route_config=route_config, type_route=type_routes)
        return (r1,r2,r3)

    def get_route_configs(self):
        route_configs:List[RouteConfig]=[]
        for rel_route_conf in [self.create_relation_route_config,self.read_all_relations_route_config,self.delete_relation_route_config]:
            if rel_route_conf is not None and rel_route_conf.route_config.is_activated:
                route_configs.append(rel_route_conf.route_config)

    def initialize_relation_route_configs_dependencies(
        self,
        authentication: Optional[AuthenticationManager] = None,
        roles: Optional[List[str]] = None,
        privileges: Optional[List[str]] = None
        )->List[RouteConfig]:
        if not authentication : return self.retrive_route_configs()
        route_configs=self.retrive_route_configs()
        for route_config in route_configs:
            if route_config.is_protected:
                route_config.dependencies = initialize_dependecies(
                    config=route_config,
                    authentication=authentication,
                    roles=roles,
                    privileges=privileges,
                )
        return route_configs

    async def get_relationship_key1(self):
        return await self.relationship_crud_models.get_attr(self.relationship_key1_name)

    async def get_relationship_key2(self):
        return await self.relationship_crud_models.get_attr(self.relationship_key2_name)

    async def get_second_model_key(self):
        return await self.second_entity_crud_models.get_attr(self.second_model_key_name)

    def check_many_to_many_class_attrs(
        self,
        relationship_crud_models: Optional[CrudModels] = None,
        relationship_key1_name: Optional[str] = None,
        relationship_key2_name: Optional[str] = None):
        if (
                relationship_crud_models is None or
                relationship_key1_name is None or
                relationship_key2_name is None
            ) :
            raise ValueError(
                "relationship_crud_models , relationship_key1_name and relationship_key2_name must be provide for relation MANY TO MANY CLASS"
            )
