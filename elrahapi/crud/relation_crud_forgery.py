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

class RelationCrudForgery:

    def __init__(
        self,
        type_relation: TypeRelation,
    ):
        self.type_relation = type_relation
        pass

    async def create_by_relation(
        self,
        session: ElrahSession,
        pk1: Any,
        create_obj: Type[BaseModel],
        entity_crud: CrudForgery,
    ):
        e1 = await entity_crud.read_one(session=session,pk=pk1)
        e2 = getattr(e1, self.relationship_name)
        if self.type_relation==TypeRelation.ONE_TO_ONE and e2 is not None:
            detail=f"{self.second_entity_crud.entity_name} already exists for {entity_crud.entity_name} with pk {pk1}"
            raise_custom_http_exception(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=detail
            )
        create_obj= self.add_fk(obj=create_obj,fk=pk1)
        new_obj = await self.second_entity_crud.create(session=session,create_obj=create_obj)
        pk2 = getattr(new_obj, self.second_entity_crud.primary_key_name)
        await self.create_relation(session=session,entity_crud=entity_crud, pk1=pk1, pk2=pk2)
        return new_obj

    async def delete_by_relation(
        self, session: ElrahSession, pk1: Any, entity_crud: CrudForgery
    ):
        entity_1 = await entity_crud.read_one(session=session,pk=pk1)
        entity_2 = getattr(entity_1, self.relationship_name)
        e2_pk = getattr(entity_2, self.second_entity_crud.primary_key_name)
        entity_2 = None
        return await self.second_entity_crud.delete(session=session,pk=e2_pk)

    async def read_one_by_relation(
        self, session: ElrahSession, pk1: Any, entity_crud: CrudForgery
    ):
        e1 = await entity_crud.read_one(session=session,pk=pk1)
        e2 = getattr(e1, self.relationship_name)
        if e2 is None :
            detail=f"{self.relationship_name} not found for {entity_crud.entity_name} with pk {pk1}"
            raise_custom_http_exception(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=detail
            )
        return e2

    async def update_by_relation(
        self,
        pk1: Any,
        session: ElrahSession,
        update_obj: Type[BaseModel],
        entity_crud: CrudForgery,
    ):
        update_obj= self.add_fk(obj=update_obj,fk=pk1)
        entity = await entity_crud.read_one(session=session,pk=pk1)
        entity_2 = getattr(entity, self.relationship_name)
        pk2 = getattr(entity_2, self.second_entity_crud.primary_key_name)
        return await self.second_entity_crud.update(
            session=session,
            pk=pk2, update_obj=update_obj, is_full_update=True
        )

    async def patch_by_relation(
        self,
        session: ElrahSession,
        pk1: Any,
        patch_obj: Type[BaseModel],
        entity_crud: CrudForgery,
    ):
        update_obj= self.add_fk(obj=update_obj,fk=pk1)
        entity = await entity_crud.read_one(session=session,pk=pk1)
        entity_2 = getattr(entity, self.relationship_name)
        pk2 = getattr(entity_2, self.second_entity_crud.primary_key_name)
        return await self.second_entity_crud.update(
            session=session,
            pk=pk2, update_obj=patch_obj, is_full_update=False
        )

    async def read_all_by_relation(
        self,
        session: ElrahSession,
        entity_crud: CrudForgery,
        pk1: Any,
        filter: Optional[str] = None,
        value: Optional[Any] = None,
        skip: int = 0,
        limit: int = None,
    ):
        e2_cm: CrudModels = self.second_entity_crud.crud_models
        e1_cm = entity_crud.crud_models
        e2_pk = e2_cm.get_pk()
        e1_pk = e1_cm.get_pk()
        if self.type_relation == TypeRelation.ONE_TO_MANY:
            stmt = (
                select(e2_cm.sqlalchemy_model)
                .join(e1_cm.sqlalchemy_model)
                .where(e1_pk == pk1)
            )
            stmt = make_filter(crud_models=e2_cm, stmt=stmt, filter=filter, value=value)
            stmt = stmt.offset(skip).limit(limit)
            results = await exec_stmt(
                session=session,
                with_scalars=True,
                stmt=stmt,
            )
            return results.all()
        elif self.type_relation == TypeRelation.MANY_TO_MANY_CLASS:
            rel_model = self.relationship_crud.crud_models.sqlalchemy_model
            rel_key1,rel_key2=self.get_relationship_keys()
            stmt = (
                select(e2_cm.sqlalchemy_model)
                .join(rel_model)
                .where(rel_key1==pk1)
            )
            stmt = make_filter(crud_models=e2_cm, stmt=stmt, filter=filter, value=value)
            stmt = stmt.offset(skip).limit(limit)
            results = await exec_stmt(
                session=session,
                with_scalars=True,
                stmt=stmt,
            )
            return results.all()
        elif self.type_relation == TypeRelation.MANY_TO_MANY_TABLE:
            rel_key1,rel_key2=self.get_relationship_keys()
            stmt = (
                    select(e2_cm.sqlalchemy_model)
                    .join(self.relation_table,e2_pk==rel_key2)
                    .join(e1_cm.sqlalchemy_model,rel_key1==e1_pk)
                    )
            stmt = make_filter(crud_models=e2_cm, stmt=stmt, filter=filter, value=value)
            stmt = stmt.offset(skip).limit(limit)
            results = await exec_stmt(
                session=session,
                with_scalars=True,
                stmt=stmt,
            )
            return results.all()
        else:
            detail = f"Operation Invalid for relation {self.type_relation}"
            raise_custom_http_exception(
                status_code=status.HTTP_400_BAD_REQUEST, detail=detail
            )
