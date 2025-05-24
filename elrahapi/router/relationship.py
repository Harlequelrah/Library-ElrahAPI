from copy import deepcopy
from typing import Any, List, Optional, Type
from elrahapi.exception.exceptions_utils import raise_custom_http_exception
from elrahapi.authentication.authentication_manager import AuthenticationManager
from elrahapi.crud.crud_models import CrudModels
from elrahapi.router.route_config import (
    AuthorizationConfig,
    ResponseModelConfig,
    RouteConfig,
)
from elrahapi.router.router_crud import (
    add_authorizations,
    initialize_dependecies,
    set_response_model_config,
    is_verified_relation_rule,
)
from elrahapi.router.router_namespace import TypeRelation
from elrahapi.router.router_routes_name import DefaultRoutesName, RelationRoutesName
from fastapi import status

from elrahapi.crud.crud_forgery import CrudForgery
from pydantic import BaseModel
from sqlalchemy.sql import Select
from sqlalchemy import and_, select
from elrahapi.utility.utils import exec_stmt, make_filter
from sqlalchemy.sql.schema import Table


class Relationship:

    def __init__(
        self,
        relationship_name: str,
        second_entity_crud: CrudForgery,
        type_relation: TypeRelation,
        relationship_crud: Optional[CrudForgery] = None,
        relationship_key1_name: Optional[str] = None,
        relationship_key2_name: Optional[str] = None,
        relations_routes_configs: Optional[RouteConfig] = None,
        relation_table: Optional[Table] = None,
        relations_authorizations_configs: Optional[AuthorizationConfig] = None,
        relations_responses_model_configs: Optional[ResponseModelConfig] = None,
        default_public_relation_routes_name: List[RelationRoutesName] = None,
        default_protected_relation_routes_name: List[RelationRoutesName] = None,
    ):
        self.relationship_name = relationship_name
        self.relationship_crud= relationship_crud
        self.second_entity_crud = second_entity_crud
        self.relationship_key1_name = relationship_key1_name
        self.relationship_key2_name = relationship_key2_name
        self.type_relation = type_relation
        self.relation_table = relation_table
        self.check_class_attrs()
        self.relations_routes_configs = self.init_routes_configs(
            default_public_relation_routes_name=default_public_relation_routes_name,
            default_protected_relation_routes_name=default_protected_relation_routes_name,
            relations_routes_configs=relations_routes_configs,
            relations_authorizations_configs=relations_authorizations_configs,
            relations_responses_model_configs=relations_responses_model_configs,
        )
        self.check_relation_rules()

    def check_relation_rules(self):
        for route_config in self.relations_routes_configs:
            if not is_verified_relation_rule(
                relation_route_name=route_config.route_name,
                type_relation=self.type_relation
                ):
                raise ValueError(
                    f" Route operation {route_config.route_name} not allowed for the relation type {self.type_relation}"
                )

    def init_default_routes(
        self,
        default_public_relation_routes_name: List[RelationRoutesName] = None,
        default_protected_relation_routes_name: List[RelationRoutesName] = None,
    ):
        default_public_relation_routes_name = default_public_relation_routes_name or []
        default_protected_relation_routes_name = (
            default_protected_relation_routes_name or []
        )
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
                    route_name=route_name,
                    route_path=path,
                    summary=f"Create {second_entity_name}",
                    description=f"Allow to create {second_entity_name}by the relation",
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
                    description=f"Allow to update {second_entity_name}by the relation",
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
                    description=f"Allow to patch {second_entity_name}by the relation",
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
                    type_relation=self.type_relation,
                    relation_route_name=route_config.route_name,
                )
                and route_config.is_activated
            ):
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
        routes_configs: List[RouteConfig] = []
        relations_authorizations_configs: List[AuthorizationConfig] = (
            relations_authorizations_configs or []
        )
        relations_responses_model_configs: List[ResponseModelConfig] = (
            relations_responses_model_configs or []
        )
        if (
            default_protected_relation_routes_name
            or default_public_relation_routes_name
        ):
            default_routes_configs = self.init_default_routes(
                default_public_relation_routes_name=default_public_relation_routes_name,
                default_protected_relation_routes_name=default_protected_relation_routes_name,
            )
            if relations_routes_configs is None:
                routes_configs = default_routes_configs
            else:
                routes_configs = (
                    deepcopy(relations_routes_configs) + default_routes_configs
                )

        purged_routes_configs = self.purge_relations(routes_configs)
        purged_routes_configs = (
            add_authorizations(
                routes_configs=purged_routes_configs,
                authorizations=relations_authorizations_configs,
            )
            if relations_authorizations_configs
            else purged_routes_configs
        )
        purged_routes_configs = (
            set_response_model_config(
                routes_config=purged_routes_configs,
                response_model_configs=relations_responses_model_configs,
            )
            if relations_responses_model_configs
            else purged_routes_configs
        )

        return purged_routes_configs

    def initialize_relation_route_configs_dependencies(
        self,
        authentication: Optional[AuthenticationManager] = None,
        roles: Optional[List[str]] = None,
        privileges: Optional[List[str]] = None,
    ) -> List[RouteConfig]:
        route_configs = self.relations_routes_configs
        if not authentication:
            route_configs
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
            return self.relationship_crud.crud_models.get_attr(self.relationship_key1_name)
        else:
            raise ValueError(
                f"relationship_key1 not available for relation type {self.type_relation}"
            )

    def get_relationship_key2(self):
        if self.type_relation == TypeRelation.MANY_TO_MANY_CLASS:
            return self.relationship_crud.crud_models.get_attr(self.relationship_key2_name)
        else:
            raise ValueError(
                f"relationship_key2 not available for relation type {self.type_relation}"
            )

    def get_second_model_key(self):
        return self.second_entity_crud.crud_models.get_pk()

    def check_class_attrs(self):
        if self.type_relation == TypeRelation.MANY_TO_MANY_CLASS and (
            self.relationship_crud.crud_models is None
            or self.relationship_key1_name is None
            or self.relationship_key2_name is None
        ):
            raise ValueError(
                "relationship_crud.crud_models , relationship_key1_name and relationship_key2_name must be provide for relation MANY TO MANY CLASS"
            )
        if self.type_relation == TypeRelation.MANY_TO_MANY_TABLE:
            if self.relation_table is None:
                raise ValueError(
                    f"Relation Table must be provide for relation {self.type_relation}"
                )

    async def create_relation(self, entity_crud: CrudForgery, pk1: Any, pk2: Any,entity_2:Optional[Any]=None):
        session = await entity_crud.session_manager.yield_session()
        entity_1 = await entity_crud.read_one(db=session, pk=pk1)
        entity_2 = await self.second_entity_crud.read_one(db=session, pk=pk2) if entity_2 is None else entity_2

        if self.type_relation == TypeRelation.ONE_TO_ONE:
            setattr(entity_1, self.relationship_name, entity_2)
        elif self.type_relation in [
            TypeRelation.MANY_TO_MANY_TABLE,
            TypeRelation.ONE_TO_MANY,
        ]:
            entity_1_attr = getattr(entity_1, self.relationship_name)
            entity_1_attr.append(entity_2)
        session.commit()
        session.refresh(entity_1)

    async def delete_relation(self, entity_crud: CrudForgery, pk1: Any, pk2: Any):
        session = await entity_crud.session_manager.yield_session()
        entity_1 = await entity_crud.read_one(db=session, pk=pk1)
        entity_2 = await self.second_entity_crud.read_one(db=session, pk=pk2)

        if self.type_relation == TypeRelation.ONE_TO_ONE:
            setattr(entity_1, self.relationship_name, None)
        elif self.type_relation in [
            TypeRelation.MANY_TO_MANY_TABLE,
            TypeRelation.ONE_TO_MANY,
        ]:
            entity_1_attr = getattr(entity_1, self.relationship_name)
            entity_1_attr.remove(entity_2)
        elif self.type_relation == TypeRelation.MANY_TO_MANY_CLASS:
            rel= await self.read_one_relation(
                pk1=pk1,
                pk2=pk2
            )
            rel_pk=getattr(rel,self.relationship_crud.primary_key_name)
            return await self.relationship_crud.delete(pk=rel_pk)
        session.commit()
        session.refresh(entity_1)

    async def read_one_relation(self,pk1:Any,pk2:Any):
        rel_key1=self.get_relationship_key1()
        rel_key2=self.get_relationship_key2()
        if self.type_relation==TypeRelation.MANY_TO_MANY_CLASS:
            session_manager = self.second_entity_crud.session_manager
            session= await session_manager.yield_session()
            stmt = select(self.relationship_crud.crud_models.sqlalchemy_model).where(
                and_(
                    rel_key1==pk1,
                    rel_key2==pk2
                )
            )
            result= await exec_stmt(
                stmt=stmt,
                session=session,
                is_async_env=session_manager.is_async_env
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
            detail = f"Bad Operation for relation {self.type_relation} of relationship {self.relationship_name}"
            raise_custom_http_exception(
                status_code=status.HTTP_400_BAD_REQUEST, detail=detail
            )

    async def create_by_relation(
        self, pk1: Any, create_obj: Type[BaseModel], entity_crud: CrudForgery
    ):
        new_obj = await self.second_entity_crud.create(create_obj=create_obj)
        pk2 = getattr(new_obj, self.second_entity_crud.primary_key_name)
        return await self.create_relation(entity_crud=entity_crud, pk1=pk1, pk2=pk2)

    async def delete_by_relation(self, pk1: Any, entity_crud: CrudForgery):
        entity_1 = await entity_crud.read_one(pk=pk1)
        entity_2 = getattr(entity_1, self.relationship_name)
        e2_pk = getattr(entity_2, self.second_entity_crud.primary_key_name)
        entity_2 = None
        return await self.second_entity_crud.delete(pk=e2_pk)

    async def read_one_by_relation(self, pk1: Any, entity_crud: CrudForgery):
        e1 = await entity_crud.read_one(pk=pk1)
        e2 = getattr(e1, self.relationship_name)
        if e2 is None :
            detail=f"{self.relationship_name} not found for {entity_crud.entity_name} with pk {pk1}"
            raise_custom_http_exception(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=detail
            )
        return e2

    async def update_by_relation(
        self, pk1: Any, update_obj: Type[BaseModel], entity_crud: CrudForgery
    ):
        entity = await entity_crud.read_one(pk=pk1)
        entity_2 = getattr(entity, self.relationship_name)
        pk2 = getattr(entity_2, self.second_entity_crud.primary_key_name)
        return await self.second_entity_crud.update(
            pk=pk2, update_obj=update_obj, is_full_updated=True
        )

    async def patch_by_relation(
        self, pk1: Any, patch_obj: Type[BaseModel], entity_crud: CrudForgery
    ):
        entity = await entity_crud.read_one(pk=pk1)
        entity_2 = getattr(entity, self.relationship_name)
        pk2 = getattr(entity_2, self.second_entity_crud.primary_key_name)
        return await self.second_entity_crud.update(
            pk=pk2, update_obj=patch_obj, is_full_updated=False
        )

    async def read_all_by_relation(
        self,
        entity_crud: CrudForgery,
        pk1: Any,
        filter: Optional[str] = None,
        value: Optional[Any] = None,
        skip: int = 0,
        limit: int = None,
    ):
        session = await entity_crud.session_manager.yield_session()
        e2_cm: CrudModels = self.second_entity_crud.crud_models
        e1_cm = entity_crud.crud_models
        e2_pk = e2_cm.get_pk()
        e1_pk = e1_cm.get_pk()
        if self.type_relation == TypeRelation.ONE_TO_MANY:
            stmt = (
                select(e2_cm.sqlalchemy_model)
                .join(e1_cm.sqlalchemy_model, e2_pk == e1_pk)
                .where(e1_pk == pk1)
            )
            stmt = make_filter(crud_models=e2_cm, stmt=stmt, filter=filter, value=value)
            stmt = stmt.offset(skip).limit(limit)
            results = await exec_stmt(
                session=session,
                is_async_env=entity_crud.session_manager.is_async_env,
                with_scalars=True,
                stmt=stmt,
            )
            return results.all()
        elif self.type_relation == TypeRelation.MANY_TO_MANY_CLASS:
            rel_model = self.relationship_crud.crud_models.sqlalchemy_model
            relkey1 = self.get_relationship_key1()
            relkey2 = self.get_relationship_key2()
            stmt = (
                select(e2_cm.sqlalchemy_model)
                .join(rel_model, e2_pk == relkey2)
                .join(e1_cm.sqlalchemy_model, relkey1 == e1_pk)
            )
            stmt = make_filter(crud_models=e2_cm, stmt=stmt, filter=filter, value=value)
            stmt = stmt.offset(skip).limit(limit)
            results = await exec_stmt(
                session=session,
                is_async_env=entity_crud.session_manager.is_async_env,
                with_scalars=True,
                stmt=stmt,
            )
            return results.all()
        elif self.type_relation == TypeRelation.MANY_TO_MANY_TABLE:
            stmt = select(e2_cm.sqlalchemy_model).join(self.relation_table)
            stmt = make_filter(crud_models=e2_cm, stmt=stmt, filter=filter, value=value)
            stmt = stmt.offset(skip).limit(limit)
            results = await exec_stmt(
                session=session,
                is_async_env=entity_crud.session_manager.is_async_env,
                with_scalars=True,
                stmt=stmt,
            )
            return results.all()
        else:
            detail = f"Operation Invalid for relation {self.type_relation}"
            raise_custom_http_exception(
                status_code=status.HTTP_400_BAD_REQUEST, detail=detail
            )
