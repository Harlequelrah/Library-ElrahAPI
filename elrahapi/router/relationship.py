from copy import deepcopy
from typing import Any, List, Optional, Type

from elrahapi.authentication.authentication_manager import AuthenticationManager
from elrahapi.crud.crud_models import CrudModels
from elrahapi.router.route_config import (
    AuthorizationConfig,
    ResponseModelConfig,
    RouteConfig,
)
from elrahapi.router.router_crud import add_authorizations, initialize_dependecies, set_response_model_config, verify_relation_rule
from elrahapi.router.router_namespace import TypeRelation
from elrahapi.router.router_routes_name import DefaultRoutesName, RelationRoutesName

from elrahapi.crud.crud_forgery import CrudForgery

from elrahapi.utility.utils import make_filter


class Relationship:

    def __init__(
        self,
        relationship_name: str,
        second_model_key_name: str,
        second_entity_crud: CrudForgery,
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
        self.second_entity_crud=second_entity_crud
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
        second_entity_name=self.second_entity_crud.second_entity_crud_models.entity_name
        path = f"/{{pk1}}/{second_entity_name}"
        for route_name in default_public_relation_routes_name+default_protected_relation_routes_name:
            if route_name==RelationRoutesName.READ_ALL_BY_RELATION:
                route_config = RouteConfig(
                    route_name=DefaultRoutesName.READ_ALL_BY_RELATION,
                    route_path=path+"s",
                    summary=f"Retrive all {second_entity_name}s",
                    description=f"Allow to retrive all {second_entity_name}s from the relation",
                    is_activated=True,
                    response_model=self.second_entity_crud.second_entity_crud_models.read_model,
                    is_protected= False if route_name in default_public_relation_routes_name else True
                )
                routes_configs.append(route_config)
            if route_name == RelationRoutesName.READ_ONE_BY_RELATION:
                route_config = RouteConfig(
                    route_name=DefaultRoutesName.READ_ONE_BY_RELATION,
                    route_path=path,
                    summary=f"Retrive {second_entity_name}",
                    description=f"Allow to retrive {second_entity_name}s from the relation",
                    is_activated=True,
                    response_model=self.second_entity_crud.second_entity_crud_models.read_model,
                    is_protected= False if route_name in default_public_relation_routes_name else True
                )
                routes_configs.append(route_config)

            if route_name == RelationRoutesName.CREATE_RELATION:
                route_config = RouteConfig(
                    route_name=DefaultRoutesName.CREATE_RELATION,
                    route_path=path + f"s/{{pk2}}",
                    summary=f"Link with {second_entity_name}",
                    description=f"Allow to link entity with {second_entity_name}",
                    is_activated=True,
                    is_protected=(
                        True
                        if route_name in default_protected_relation_routes_name
                        else False
                    ),
                )
                routes_configs.append(route_config)
            if route_name == RelationRoutesName.DELETE_RELATION:
                route_config = RouteConfig(
                    route_name=DefaultRoutesName.DELETE_RELATION,
                    route_path=path + f"s/{{pk2}}",
                    summary=f"Unlink with {second_entity_name}",
                    description=f"Allow to unlink entity with {second_entity_name}",
                    is_activated=True,
                    is_protected=(
                        True
                        if route_name in default_protected_relation_routes_name
                        else False
                    ),
                )
                routes_configs.append(route_config)

            if route_name == RelationRoutesName.DELETE_BY_RELATION:
                route_config = RouteConfig(
                    route_name=DefaultRoutesName.DELETE_BY_RELATION,
                    route_path=path,
                    summary=f"Delete {second_entity_name}",
                    description=f"Allow to delete {second_entity_name}by the relation",
                    is_activated=True,
                    is_protected=(
                        True
                        if route_name in default_protected_relation_routes_name
                        else False
                    ),
                )
                routes_configs.append(route_config)

            if route_name == RelationRoutesName.CREATE_BY_RELATION:
                route_config = RouteConfig(
                    route_name=DefaultRoutesName.CREATE_BY_RELATION,
                    route_path=path,
                    summary=f"Create {second_entity_name}",
                    description=f"Allow to create {second_entity_name}by the relation",
                    is_activated=True,
                    is_protected=(
                        True
                        if route_name in default_protected_relation_routes_name
                        else False
                    ),
                    response_model=self.second_entity_crud.second_entity_crud_models.read_model,
                )
                routes_configs.append(route_config)

            if route_name == RelationRoutesName.UPDATE_BY_RELATION:
                route_config = RouteConfig(
                    route_name=DefaultRoutesName.UPDATE_BY_RELATION,
                    route_path=path,
                    summary=f"Update {second_entity_name}",
                    description=f"Allow to update {second_entity_name}by the relation",
                    is_activated=True,
                    is_protected=(
                        True
                        if route_name in default_protected_relation_routes_name
                        else False
                    ),
                    response_model=self.second_entity_crud.second_entity_crud_models.read_model,
                )
                routes_configs.append(route_config)

            if route_name == RelationRoutesName.PATCH_BY_RELATION:
                route_config = RouteConfig(
                    route_name=DefaultRoutesName.PATCH_BY_RELATION,
                    route_path=path,
                    summary=f"Patch {second_entity_name}",
                    description=f"Allow to patch {second_entity_name}by the relation",
                    is_activated=True,
                    is_protected=(
                        True
                        if route_name in default_protected_relation_routes_name
                        else False
                    ),
                    response_model=self.second_entity_crud.second_entity_crud_models.read_model,
                )
                routes_configs.append(route_config)
        return routes_configs

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
        relations_authorizations_configs: Optional[List[AuthorizationConfig]] = None,
        relations_responses_model_configs: Optional[ResponseModelConfig] = None,
        default_public_relation_routes_name: List[RelationRoutesName] = None,
        default_protected_relation_routes_name: List[RelationRoutesName] = None,
    ):
        routes_configs:List[RouteConfig]=[]
        relations_authorizations_configs: List[AuthorizationConfig] = relations_authorizations_configs or []
        relations_responses_model_configs: List[ResponseModelConfig] = relations_responses_model_configs or []
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
        purged_routes_configs = add_authorizations(
            routes_configs=purged_routes_configs,
            authorizations=relations_authorizations_configs
            ) if relations_authorizations_configs else purged_routes_configs
        purged_routes_configs =set_response_model_config(
            routes_config=purged_routes_configs,
            response_model_configs=relations_responses_model_configs,
        ) if relations_responses_model_configs else purged_routes_configs

        return purged_routes_configs

    def initialize_relation_route_configs_dependencies(
        self,
        authentication: Optional[AuthenticationManager] = None,
        roles: Optional[List[str]] = None,
        privileges: Optional[List[str]] = None
        )->List[RouteConfig]:
        route_configs= self.relations_routes_configs
        if not authentication : route_configs
        for route_config in route_configs:
            if route_config.is_protected:
                route_config.dependencies = initialize_dependecies(
                    config=route_config,
                    authentication=authentication,
                    roles=roles,
                    privileges=privileges,
                )
        return route_configs

    def get_relationship_key1(self):
        if self.type_relation == TypeRelation.MANY_TO_MANY_CLASS:
            return  self.relationship_crud_models.get_attr(self.relationship_key1_name)
        else :
            raise ValueError(f"relationship_key1 not available for relation type {self.type_relation}")

    def get_relationship_key2(self):
        if self.type_relation == TypeRelation.MANY_TO_MANY_CLASS:
            return  self.relationship_crud_models.get_attr(self.relationship_key2_name)
        else:
            raise ValueError(
                f"relationship_key2 not available for relation type {self.type_relation}"
            )

    def get_second_model_key(self):
        return  self.second_entity_crud.second_entity_crud_models.get_attr(self.second_model_key_name)

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

    async def create_relation(self,entity_crud:CrudForgery,pk1:Any,pk2:Any):
        session=entity_crud.session_manager.yield_session()
        entity_1=entity_crud.read_one(db=session,pk=pk1)
        entity_2=self.second_entity_crud.read_one(db=session,pk=pk2)

        if self.type_relation == TypeRelation.ONE_TO_ONE:
            setattr(entity_1, self.relationship_name, entity_2)
        elif self.type_relation in [
            TypeRelation.MANY_TO_MANY_TABLE,
            TypeRelation.ONE_TO_MANY
        ]:
            entity_1_attr=getattr(entity_1,self.relationship_name)
            entity_1_attr.append(entity_2)
        else : raise ValueError(f"Operation not allowed for the relation type {self.type_relation}")
        session.commit()
        session.refresh(entity_1)

    async def delete_relation(self, entity_crud: CrudForgery, pk1: Any, pk2: Any):
        session = entity_crud.session_manager.yield_session()
        entity_1 = entity_crud.read_one(db=session, pk=pk1)
        entity_2 = self.second_entity_crud.read_one(db=session, pk=pk2)

        if self.type_relation == TypeRelation.ONE_TO_ONE:
            setattr(entity_1, self.relationship_name, None)
        elif self.type_relation in [
            TypeRelation.MANY_TO_MANY_TABLE,
            TypeRelation.ONE_TO_MANY,
        ]:
            entity_1_attr = getattr(entity_1, self.relationship_name)
            entity_1_attr.remove(entity_2)
        else : raise ValueError(f"Operation not allowed for the relation type {self.type_relation}")
        session.commit()
        session.refresh(entity_1)


        # async def read_all_by_relation(
        #     self,
        #     entity_crud:CrudForgery,
        #     pk1: Any,
        #     filter: Optional[str] = None,
        #     value: Optional[Any] = None,
        #     skip: int = 0,
        #     limit: int = None,
        # ):
        #     session=entity_crud.session_manager.yield_session()
        #     entity=entity_crud.read_one(pk=pk1)
        #     relations=getattr(entity,self.relationship_name)
        #     if self.type_relation in [
        #         TypeRelation.ONE_TO_MANY,
        #         TypeRelation.MANY_TO_MANY_TABLE]:
        #         return relations

        #     elif self.type_relation==TypeRelation.MANY_TO_MANY_CLASS:
        #         e1_cm:CrudModels=entity_crud.crud_models
        #         e2_cm:CrudModels=self.second_entity_crud.crud_models
        #         e1_pk=  e1_cm.get_pk()
        #         e2_pk =  e2_cm.get_pk()
        #         relkey1 =  self.get_relationship_key1()
        #         relkey2 =  self.get_relationship_key2()
        #         rel_model=self.relationship_crud_models.sqlalchemy_model
        #         query=(
        #             session.query(e2_cm.sqlalchemy_model)
        #             .join(rel_model,relkey2==e2_pk)
        #             .join(e1_cm.sqlalchemy_model,
        #                 relkey1==e1_pk
        #                 )
        #             )
        #         query=make_filter(
        #             crud_models=e2_cm,
        #             query=query,
        #             filter=filter,
        #             value=value
        #         )
        #         results=query.offset(skip).limit(limit).all()
        #         return results


