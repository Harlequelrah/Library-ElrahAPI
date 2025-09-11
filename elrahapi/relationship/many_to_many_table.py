from typing import Any, Type

from elrahapi.crud.crud_forgery import CrudForgery
from elrahapi.crud.crud_models import CrudModels
from elrahapi.exception.exceptions_utils import raise_custom_http_exception
from elrahapi.relationship.base_relationship import BaseRelationship
from elrahapi.router.route_additional_config import (
    AuthorizationConfig,
    ResponseModelConfig,
)
from elrahapi.router.route_config import RouteConfig
from elrahapi.router.router_routes_name import RelationRoutesName
from elrahapi.utility.types import ElrahSession
from elrahapi.utility.utils import apply_filters, exec_stmt, get_filters
from pydantic import BaseModel
from sqlalchemy import Table, select

from fastapi import Depends, Request, status


class ManyToManyTableRelationship(BaseRelationship):
    RELATION_RULES = [
        RelationRoutesName.READ_ALL_BY_RELATION,
        RelationRoutesName.CREATE_RELATION,
        RelationRoutesName.DELETE_RELATION,
        RelationRoutesName.CREATE_BY_RELATION,
    ]

    def __init__(
        self,
        relationship_name: str,
        second_entity_crud: CrudForgery,
        relationship_key1_name: str | None = None,
        relationship_key2_name: str | None = None,
        relation_table: Table | None = None,
        relations_routes_configs: list[RouteConfig] | None = None,
        second_entity_fk_name: str | None = None,
        relations_authorizations_configs: AuthorizationConfig | None = None,
        relations_responses_model_configs: ResponseModelConfig | None = None,
        default_public_relation_routes_name: list[RelationRoutesName] | None = None,
        default_protected_relation_routes_name: list[RelationRoutesName] | None = None,
    ):
        super().__init__(
            second_entity_crud=second_entity_crud,
            relationship_name=relationship_name,
            second_entity_crud=second_entity_crud,
            second_entity_fk_name=second_entity_fk_name,
            relations_routes_configs=relations_routes_configs,
            default_public_relation_routes_name=default_public_relation_routes_name,
            default_protected_relation_routes_name=default_protected_relation_routes_name,
            relations_authorizations_configs=relations_authorizations_configs,
            relations_responses_model_configs=relations_responses_model_configs,
        )
        self.relationship_key1_name = relationship_key1_name
        self.relationship_key2_name = relationship_key2_name
        self.relation_table = relation_table

    def get_relationship_keys(self):
        columns = self.relation_table.c
        rel_key1 = getattr(columns, self.relationship_key1_name)
        rel_key2 = getattr(columns, self.relationship_key2_name)
        return rel_key1, rel_key2

    def create_relation(self, entity_crud: CrudForgery):
        async def endpoint(
            pk1: Any, pk2: Any, session: ElrahSession = Depends(self.yield_session)
        ):
            entity_1 = await entity_crud.read_one(session=session, pk=pk1)
            entity_2 = await self.second_entity_crud.read_one(session=session, pk=pk2)
            entity_1_attr = getattr(entity_1, self.relationship_name)
            entity_1_attr.append(entity_2)
            await entity_crud.session_manager.commit_and_refresh(
                session=session, object=entity_1
            )

        return endpoint

    def delete_relation(
        self,
        entity_crud: CrudForgery,
    ):

        async def endpoint(
            pk1: Any,
            pk2: Any,
            session: ElrahSession = Depends(self.yield_session),
        ):
            entity_1 = await entity_crud.read_one(session=session, pk=pk1)
            entity_2 = await self.second_entity_crud.read_one(session=session, pk=pk2)
            entity_1_attr = getattr(entity_1, self.relationship_name)
            if entity_2 in entity_1_attr:
                entity_1_attr.remove(entity_2)
                await entity_crud.session_manager.commit_and_refresh(
                    session=session, object=entity_1
                )
            else:
                detail = f"Relation between {entity_crud.entity_name} with pk {pk1} and {self.second_entity_crud.entity_name} with pk {pk2} not found"
                raise_custom_http_exception(
                    status_code=status.HTTP_404_NOT_FOUND, detail=detail
                )

        return endpoint

    def create_by_relation(
        self,
        entity_crud: CrudForgery,
    ):
        async def endpoint(
            pk1: Any,
            create_obj: Type[BaseModel],
            session: ElrahSession = Depends(self.yield_session),
        ):
            create_obj = self.add_fk(obj=create_obj, fk=pk1)
            new_obj = await self.second_entity_crud.create(
                session=session, create_obj=create_obj
            )
            pk2 = getattr(new_obj, self.second_entity_crud.primary_key_name)
            await self.create_relation(
                session=session, entity_crud=entity_crud, pk1=pk1, pk2=pk2
            )
            return new_obj

        return endpoint

    def delete_by_relation(self, entity_crud: CrudForgery):
        async def endpoint(
            pk1: Any, pk2: Any, session: ElrahSession = Depends(self.yield_session)
        ):
            self.delete_relation(
                session=session, entity_crud=entity_crud, pk1=pk1, pk2=pk2
            )
            return await self.second_entity_crud.delete(session=session, pk=pk2)

        return endpoint

    def read_all_by_relation(
        self,
        entity_crud: CrudForgery,
    ):
        async def endpoint(
            request: Request,
            pk1: Any,
            skip: int = 0,
            limit: int = None,
            session: ElrahSession = Depends(self.yield_session),
        ):
            filters = get_filters(request=request)
            e2_cm: CrudModels = self.second_entity_crud.crud_models
            e1_cm = entity_crud.crud_models
            e1_pk = e1_cm.get_pk()
            e2_pk = e2_cm.get_pk()
            rel_key1, rel_key2 = self.get_relationship_keys()
            stmt = (
                select(e2_cm.sqlalchemy_model)
                .join(self.relation_table, e2_pk == rel_key2)
                .join(e1_cm.sqlalchemy_model, rel_key1 == e1_pk)
                .where(e1_pk == pk1)
            )
            stmt = apply_filters(crud_models=e2_cm, stmt=stmt, filters=filters)
            stmt = stmt.offset(skip).limit(limit)
            results = await exec_stmt(
                session=session,
                with_scalars=True,
                stmt=stmt,
            )
            return results.all()

        return endpoint
