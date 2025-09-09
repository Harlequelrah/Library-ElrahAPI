from typing import Any, Type

from elrahapi.crud.crud_forgery import CrudForgery
from elrahapi.exception.exceptions_utils import raise_custom_http_exception
from elrahapi.relationship.base_relationship import BaseRelationship
from elrahapi.router.route_additional_config import (
    AuthorizationConfig,
    ResponseModelConfig,
)
from elrahapi.router.route_config import RouteConfig
from elrahapi.router.router_routes_name import RelationRoutesName
from elrahapi.utility.types import ElrahSession
from pydantic import BaseModel

from fastapi import status


class OneToManyRelationShip(BaseRelationship):
    def __init__(
        self,
        relationship_name: str,
        second_entity_crud: CrudForgery,
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

    async def create_relation(
        self, session: ElrahSession, entity_crud: CrudForgery, pk1: Any, pk2: Any
    ):
        entity_1 = await entity_crud.read_one(session=session, pk=pk1)
        entity_2 = await self.second_entity_crud.read_one(session=session, pk=pk2)
        entity_1_attr = getattr(entity_1, self.relationship_name)
        entity_1_attr.append(entity_2)
        await entity_crud.session_manager.commit_and_refresh(
            session=session, object=entity_1
        )

    async def delete_relation(
        self, session: ElrahSession, entity_crud: CrudForgery, pk1: Any, pk2: Any
    ):
        entity_1 = await entity_crud.read_one(session=session, pk=pk1)
        entity_2 = await self.second_entity_crud.read_one(session=session, pk=pk2)
        entity_1_attr = getattr(entity_1, self.relationship_name)
        if entity_2 in entity_1_attr:
            entity_1_attr.remove(entity_2)
            await entity_crud.session_manager.commit_and_refresh(
                session=session, object=entity_1
            )

    async def create_by_relation(
        self,
        session: ElrahSession,
        pk1: Any,
        create_obj: Type[BaseModel],
        entity_crud: CrudForgery,
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

    async def delete_by_relation(
        self, session: ElrahSession, pk1: Any, entity_crud: CrudForgery, pk2: Any
    ):
        self.delete_relation(session=session, entity_crud=entity_crud, pk1=pk1, pk2=pk2)
        return await self.second_entity_crud.delete(session=session, pk=pk2)

    async def soft_delete_by_relation(self, session: ElrahSession, pk: Any):
        return await self.second_entity_crud.soft_delete(session=session, pk=pk)

    async def read_one_by_relation(self, session: ElrahSession, pk: Any):
        return self.second_entity_crud.read_one(session=session, pk=pk)

    async def update_by_relation(
        self,
        pk1: Any,
        pk2: Any,
        session: ElrahSession,
        update_obj: Type[BaseModel],
    ):
        update_obj = self.add_fk(obj=update_obj, fk=pk1)
        return await self.second_entity_crud.update(
            session=session, pk=pk2, update_obj=update_obj, is_full_update=True
        )

    async def patch_by_relation(
        self,
        session: ElrahSession,
        pk1: Any,
        pk2: Any,
        patch_obj: Type[BaseModel],
        entity_crud: CrudForgery,
    ):
        update_obj = self.add_fk(obj=update_obj, fk=pk1)
        return await self.second_entity_crud.update(
            session=session, pk=pk2, update_obj=patch_obj, is_full_update=False
        )
