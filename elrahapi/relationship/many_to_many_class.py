from copy import deepcopy
from typing import Any

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
from sqlalchemy import  select

from fastapi import Depends, Request, status


class ManyToManyClassRelationship(BaseRelationship):
    RELATION_RULES = [
        RelationRoutesName.READ_ALL_BY_RELATION,
        RelationRoutesName.DELETE_RELATION,
        RelationRoutesName.READ_ONE_RELATION,
    ]

    def __init__(
        self,
        relationship_name: str,
        second_entity_crud: CrudForgery,
        relationship_key1_name: str,
        relationship_key2_name: str,
        relationship_crud: CrudForgery | None = None,
        relations_routes_configs: list[RouteConfig] | None = None,
        relations_authorizations_configs: AuthorizationConfig | None = None,
        relations_responses_model_configs: ResponseModelConfig | None = None,
        default_public_relation_routes_name: list[RelationRoutesName] | None = None,
        default_protected_relation_routes_name: list[RelationRoutesName] | None = None,
    ):
        super().__init__(
            second_entity_crud=second_entity_crud,
            relationship_name=relationship_name,
            relations_routes_configs=relations_routes_configs,
            default_public_relation_routes_name=default_public_relation_routes_name,
            default_protected_relation_routes_name=default_protected_relation_routes_name,
            relations_authorizations_configs=relations_authorizations_configs,
            relations_responses_model_configs=relations_responses_model_configs,
        )
        self.relationship_key1_name = relationship_key1_name
        self.relationship_key2_name = relationship_key2_name
        self.relationship_crud = relationship_crud

    def get_relationship_keys(self):
        rel_key1 = self.relationship_crud.crud_models.get_attr(
            self.relationship_key1_name
        )
        rel_key2 = self.relationship_crud.crud_models.get_attr(
            self.relationship_key2_name
        )
        return rel_key1, rel_key2

    def init_default_routes(self):
        routes_configs: list[RouteConfig] = super().init_default_routes()
        copied_routes_configs = deepcopy(routes_configs)
        if (
            RelationRoutesName.READ_ONE_RELATION
            in self.default_public_relation_routes_name
            + self.default_protected_relation_routes_name
        ):
            e2_name = self.second_entity_crud.entity_name
            route_config = RouteConfig(
                route_name=RelationRoutesName.READ_ONE_RELATION,
                route_path=f"/{{pk1}}/{e2_name}s/{{pk2}}",
                summary=f"Read one {self.relationship_name} relation",
                description=f"Allow to read relation with {e2_name} ",
                is_activated=True,
                is_protected=(
                    True
                    if RelationRoutesName.READ_ONE_RELATION
                    in self.default_protected_relation_routes_name
                    else False
                ),
                response_model=self.relationship_crud.crud_models.read_model,
            )
            copied_routes_configs.append(route_config)
        return copied_routes_configs

    def delete_relation(self, entity_crud: CrudForgery):
        async def endpoint(
            pk1: Any, pk2: Any, session: ElrahSession = Depends(self.yield_session)
        ):
            rel = await self.read_one_relation_crud(session=session, pk1=pk1, pk2=pk2)
            rel_pk = getattr(rel, self.relationship_crud.primary_key_name)
            return await self.relationship_crud.delete(session=session, pk=rel_pk)

        return endpoint

    async def read_one_relation_crud(
        self, pk1: Any, pk2: Any, session: ElrahSession, with_deleted: bool = False
    ):
        rel_key1, rel_key2 = self.get_relationship_keys()
        conditions = [rel_key1 == pk1, rel_key2 == pk2]
        if not with_deleted:
            conditions.append(
                self.relationship_crud.SQLAlchemyModel.is_deleted == False
            )
        stmt = select(self.relationship_crud.crud_models.sqlalchemy_model).where(
            *conditions
        )
        result = await exec_stmt(
            stmt=stmt,
            session=session,
        )
        rel = result.scalar_one_or_none()
        if rel is None:
            detail = f"Relation of {self.relationship_name} with IDs ({pk1},{pk2}) is not found "
            raise_custom_http_exception(
                status_code=status.HTTP_404_NOT_FOUND, detail=detail
            )
        return rel

    def read_one_relation(self, entity_crud: CrudForgery):
        async def endpoint(
            pk1: Any,
            pk2: Any,
            with_deleted: bool | None = None,
            session: ElrahSession = Depends(self.yield_session),
        ):
            return await self.read_one_relation_crud(
                pk1=pk1, pk2=pk2, session=session, with_deleted=with_deleted
            )

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
            rel_model = self.relationship_crud.crud_models.sqlalchemy_model
            rel_key1, rel_key2 = self.get_relationship_keys()
            stmt = select(e2_cm.sqlalchemy_model).join(rel_model).where(rel_key1 == pk1)
            stmt = apply_filters(
                crud_models=e2_cm,
                stmt=stmt,
                filters=filters,
            )
            stmt = stmt.offset(skip).limit(limit)
            results = await exec_stmt(
                session=session,
                with_scalars=True,
                stmt=stmt,
            )
            return results.all()

        return endpoint
