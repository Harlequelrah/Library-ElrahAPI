from copy import deepcopy
from typing import Any, List, Optional, Type
from elrahapi.utility.types import ElrahSession
from elrahapi.exception.custom_http_exception import CustomHttpException
from elrahapi.authentication.authentication_manager import AuthenticationManager
from elrahapi.crud.crud_forgery import CrudForgery
from elrahapi.crud.crud_models import CrudModels
from elrahapi.exception.exceptions_utils import raise_custom_http_exception
from elrahapi.router.route_config import (
    AuthorizationConfig,
    ResponseModelConfig,
    RouteConfig,
)
from elrahapi.router.router_crud import (
    add_authorizations,
    initialize_dependecies,
    is_verified_relation_rule,
    set_response_model_config,
)
from elrahapi.router.router_namespace import TypeRelation
from elrahapi.router.router_routes_name import RelationRoutesName
from elrahapi.utility.utils import exec_stmt, make_filter, validate_value
from pydantic import BaseModel
from sqlalchemy import and_, select

from fastapi import status
from sqlalchemy.sql.schema import Table

from elrahapi.crud.relation_crud_forgery import RelationCrudForgery
class Relationship:

    def __init__(
        self,
        relationship_name: str,
        relation_crud:RelationCrudForgery,

        second_entity_crud: CrudForgery,
        relationship_crud: Optional[CrudForgery] = None,
        relationship_key1_name: Optional[str] = None,
        relationship_key2_name: Optional[str] = None,
        relations_routes_configs: Optional[RouteConfig] = None,
        relation_table: Optional[Table] = None,
        second_entity_fk_name: Optional[str] = None,
        relations_authorizations_configs: Optional[AuthorizationConfig] = None,
        relations_responses_model_configs: Optional[ResponseModelConfig] = None,
        default_public_relation_routes_name: List[RelationRoutesName] = None,
        default_protected_relation_routes_name: List[RelationRoutesName] = None,
    ):
        self.relationship_name = relationship_name
        self.second_entity_fk_name=second_entity_fk_name
        self.relationship_name = relationship_name
        self.relationship_crud= relationship_crud
        self.second_entity_crud = second_entity_crud
        self.relationship_key1_name = relationship_key1_name
        self.relationship_key2_name = relationship_key2_name
        self.relation_table = relation_table
        self.relations_routes_configs = relations_routes_configs or []
        self.default_public_relation_routes_name=default_public_relation_routes_name or []
        self.default_protected_relation_routes_name=default_protected_relation_routes_name or []
        self.relations_authorizations_configs=relations_authorizations_configs or []
        self.relations_responses_model_configs=relations_responses_model_configs or []
        self.check_relation_rules()

    def get_second_model_key(self):
        return self.second_entity_crud.crud_models.get_pk()

    def get_relationship_keys(self):
        if self.relation_crud.type_relation == TypeRelation.MANY_TO_MANY_CLASS:
            rel_key1= self.relationship_crud.crud_models.get_attr(self.relationship_key1_name)
            rel_key2=self.relationship_crud.crud_models.get_attr(self.relationship_key2_name)
            return rel_key1,rel_key2
        elif self.relation_crud.type_relation == TypeRelation.MANY_TO_MANY_TABLE:
            if self.relation_table is not None:
                columns= self.relation_table.c
                rel_key1 = getattr(columns, self.relationship_key1_name)
                rel_key2 = getattr(columns, self.relationship_key2_name)
                return rel_key1, rel_key2
        else:
            raise ValueError(
                f"relationship_keys not available for relation type {self.relation_crud.type_relation}"
            )

    def check_relation_rules(self):
        for route_config in self.relations_routes_configs:
            if not is_verified_relation_rule(
                relation_route_name=route_config.route_name,
                type_relation=self.relation_crud.type_relation
                ):
                raise ValueError(
                    f" Route operation {route_config.route_name} not allowed for the relation type {self.relation_crud.type_relation}"
                )

    def init_default_routes(
        self,
        default_public_relation_routes_name: List[RelationRoutesName],
        default_protected_relation_routes_name: List[RelationRoutesName] ,
    ):
        full_routes_configs = (
            default_public_relation_routes_name + default_protected_relation_routes_name
        )
        routes_configs: List[RouteConfig] = []
        second_entity_name = self.second_entity_crud.entity_name
        path = f"/{{pk1}}/{second_entity_name}"
        for route_name in full_routes_configs:
            if route_name == RelationRoutesName.READ_ALL_BY_RELATION:
                route_config = RouteConfig(
                    route_name=route_name,
                    route_path=path + "s",
                    summary=f"Retrive all {second_entity_name}s",
                    description=f"Allow to retrive all {second_entity_name}s from the relation",
                    is_activated=True,
                    response_model=self.second_entity_crud.crud_models.read_model,
                    is_protected=(
                        False
                        if route_name in default_public_relation_routes_name
                        else True
                    ),
                )
                routes_configs.append(route_config)
            if route_name == RelationRoutesName.READ_ONE_BY_RELATION:
                route_config = RouteConfig(
                    route_name=route_name,
                    route_path=path,
                    summary=f"Retrive {second_entity_name}",
                    description=f"Allow to retrive {second_entity_name}s from the relation",
                    is_activated=True,
                    response_model=self.second_entity_crud.crud_models.read_model,
                    is_protected=(
                        False
                        if route_name in default_public_relation_routes_name
                        else True
                    ),
                )
                routes_configs.append(route_config)

            if route_name == RelationRoutesName.CREATE_RELATION:
                route_config = RouteConfig(
                    route_name=route_name,
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
                    route_name=route_name,
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
                    route_name=route_name,
                    route_path=path,
                    summary=f"Delete {second_entity_name}",
                    description=f"Allow to delete {second_entity_name} by the relation",
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
                    route_name=route_name,
                    route_path=path,
                    summary=f"Create {second_entity_name}",
                    description=f"Allow to create {second_entity_name} by the relation",
                    is_activated=True,
                    is_protected=(
                        True
                        if route_name in default_protected_relation_routes_name
                        else False
                    ),
                    response_model=self.second_entity_crud.crud_models.read_model,
                )
                routes_configs.append(route_config)

            if route_name == RelationRoutesName.UPDATE_BY_RELATION:
                route_config = RouteConfig(
                    route_name=route_name,
                    route_path=path,
                    summary=f"Update {second_entity_name}",
                    description=f"Allow to update {second_entity_name} by the relation",
                    is_activated=True,
                    is_protected=(
                        True
                        if route_name in default_protected_relation_routes_name
                        else False
                    ),
                    response_model=self.second_entity_crud.crud_models.read_model,
                )
                routes_configs.append(route_config)

            if route_name == RelationRoutesName.PATCH_BY_RELATION:
                route_config = RouteConfig(
                    route_name=route_name,
                    route_path=path,
                    summary=f"Patch {second_entity_name}",
                    description=f"Allow to patch {second_entity_name} by the relation",
                    is_activated=True,
                    is_protected=(
                        True
                        if route_name in default_protected_relation_routes_name
                        else False
                    ),
                    response_model=self.second_entity_crud.crud_models.read_model,
                )
                routes_configs.append(route_config)
        return routes_configs

    def purge_relations(self, routes_configs: List[RouteConfig]):
        purged_routes_configs: List[RouteConfig] = []
        for route_config in routes_configs:
            if (
                is_verified_relation_rule(
                    type_relation=self.relation_crud.type_relation,
                    relation_route_name=route_config.route_name,
                )
                and route_config.is_activated
            ):
                purged_routes_configs.append(route_config)
        return purged_routes_configs

    def init_routes_configs(
        self,
        authentication: Optional[AuthenticationManager] = None,
        roles: Optional[List[str]] = None,
        privileges: Optional[List[str]] = None,
    ):
        routes_configs: List[RouteConfig] = []
        if (
            self.default_protected_relation_routes_name
            or self.default_public_relation_routes_name
        ):
            default_routes_configs = self.init_default_routes(
                default_public_relation_routes_name= self.default_public_relation_routes_name,
                default_protected_relation_routes_name=self.default_protected_relation_routes_name,
            )
            if not self.relations_routes_configs:
                routes_configs = default_routes_configs
            else:
                routes_configs = (
                    deepcopy(self.relations_routes_configs) + default_routes_configs
                )

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
            set_response_model_config(
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
        routes_configs: List[RouteConfig],
        authentication: Optional[AuthenticationManager] = None,
        roles: Optional[List[str]] = None,
        privileges: Optional[List[str]] = None,
    ) -> List[RouteConfig]:
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

    async def create_relation(self,session:ElrahSession,entity_crud: CrudForgery, pk1: Any, pk2: Any):
        entity_1 = await entity_crud.read_one(session=session, pk=pk1)
        entity_2 = await self.second_entity_crud.read_one(session=session, pk=pk2)
        if self.relation_crud.type_relation == TypeRelation.ONE_TO_ONE:
            setattr(entity_1, self.relationship_name, entity_2)
        elif self.relation_crud.type_relation in [
            TypeRelation.MANY_TO_MANY_TABLE,
            TypeRelation.ONE_TO_MANY,
        ]:
            entity_1_attr = getattr(entity_1, self.relationship_name)
            entity_1_attr.append(entity_2)
        await entity_crud.session_manager.commit_and_refresh(
            session=session,
            object=entity_1
        )


    async def delete_relation(
        self, session: ElrahSession, entity_crud: CrudForgery, pk1: Any, pk2: Any
    ):
        entity_1 = await entity_crud.read_one(session=session, pk=pk1)
        entity_2 = await self.second_entity_crud.read_one(session=session, pk=pk2)

        if self.relation_crud.type_relation == TypeRelation.ONE_TO_ONE:
            setattr(entity_1, self.relationship_name, None)
            await entity_crud.session_manager.commit_and_refresh(
            session=session,
            object=entity_1
            )
        elif self.relation_crud.type_relation in [
            TypeRelation.MANY_TO_MANY_TABLE,
            TypeRelation.ONE_TO_MANY,
        ]:
            entity_1_attr = getattr(entity_1, self.relationship_name)
            if entity_2 in entity_1_attr:
                entity_1_attr.remove(entity_2)
                await entity_crud.session_manager.commit_and_refresh(
                    session=session,
                    object=entity_1
                    )
            else:
                detail = f"Relation between {entity_crud.entity_name} with pk {pk1} and {self.second_entity_crud.entity_name} with pk {pk2} not found"
                raise_custom_http_exception(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=detail
                )
        elif self.relation_crud.type_relation == TypeRelation.MANY_TO_MANY_CLASS:
            rel= await self.read_one_relation(
                session=session,
                pk1=pk1,
                pk2=pk2
            )
            rel_pk=getattr(rel,self.relationship_crud.primary_key_name)
            return await self.relationship_crud.delete(session=session,pk=rel_pk)


    async def read_one_relation(self, session: ElrahSession, pk1: Any, pk2: Any):
        rel_key1,rel_key2=self.get_relationship_keys()
        if self.relation_crud.type_relation==TypeRelation.MANY_TO_MANY_CLASS:
            stmt = select(self.relationship_crud.crud_models.sqlalchemy_model).where(
                and_(
                    rel_key1==pk1,
                    rel_key2==pk2
                )
            )
            result= await exec_stmt(
                stmt=stmt,
                session=session,
            )
            rel = result.scalar_one_or_none()
            if rel is None:
                detail=f"Relation of {self.relationship_name} with IDs ({pk1},{pk2}) is not found "
                raise_custom_http_exception(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=detail
                )
            return rel
        else :
            detail = f"Bad Operation for relation {self.relation_crud.type_relation} of relationship {self.relationship_name}"
            raise_custom_http_exception(
                status_code=status.HTTP_400_BAD_REQUEST, detail=detail
            )

    def add_fk(self,obj:Type[BaseModel],fk:Any):
        if self.second_entity_fk_name is not None:
            validated_fk=validate_value(value=fk)
            new_obj= obj.model_copy(update={self.second_entity_fk_name:validated_fk})
            return new_obj
        return obj

