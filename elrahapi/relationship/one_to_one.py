from copy import deepcopy
from typing import Any

from elrahapi.crud.crud_forgery import CrudForgery
from elrahapi.exception.exceptions_utils import raise_custom_http_exception
from elrahapi.relationship.base_relationship import BaseRelationship
from elrahapi.router.route_additional_config import (
    AuthorizationConfig,
    ResponseModelConfig,
)
from elrahapi.router.route_config import RouteConfig
from elrahapi.router.router_crud import exclude_route
from elrahapi.router.router_routes_name import RelationRoutesName
from elrahapi.utility.types import ElrahSession

from fastapi import Depends, status


class OneToOneRelationship(BaseRelationship):
    RELATION_RULES = [
        RelationRoutesName.READ_ONE_BY_RELATION,
        RelationRoutesName.CREATE_RELATION,
        RelationRoutesName.DELETE_RELATION,
        RelationRoutesName.CREATE_BY_RELATION,
        RelationRoutesName.UPDATE_BY_RELATION,
        RelationRoutesName.PATCH_BY_RELATION,
        RelationRoutesName.SOFT_DELETE_BY_RELATION,
        RelationRoutesName.DELETE_BY_RELATION,
    ]

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
        super().__init__(
            relationship_name=relationship_name,
            second_entity_crud=second_entity_crud,
            relations_routes_configs=relations_routes_configs,
            default_public_relation_routes_name=default_public_relation_routes_name,
            default_protected_relation_routes_name=default_protected_relation_routes_name,
            relations_authorizations_configs=relations_authorizations_configs,
            relations_responses_model_configs=relations_responses_model_configs,
        )

    def init_default_routes(self):
        routes_configs = super().init_default_routes()
        copied_routes_configs = exclude_route(
            routes=deepcopy(routes_configs),
            exclude_routes_name=[RelationRoutesName.DELETE_RELATION],
        )
        second_entity_name = self.second_entity_crud.entity_name
        route_config = RouteConfig(
            route_name=RelationRoutesName.DELETE_RELATION,
            route_path=f"/{{pk1}}/{second_entity_name}s",
            summary=f"delete one {self.relationship_name} relation",
            description=f"Allow to unlink with {second_entity_name}",
            is_activated=True,
            is_protected=(
                True
                if RelationRoutesName.DELETE_RELATION
                in self.default_protected_relation_routes_name
                else False
            ),
        )
        copied_routes_configs.append(route_config)
        return copied_routes_configs

    async def create_relation_crud(
        self, pk1: Any, pk2: Any, session: ElrahSession, entity_crud: CrudForgery
    ):
        entity_1 = await entity_crud.read_one(session=session, pk=pk1)
        entity_2 = await self.second_entity_crud.read_one(session=session, pk=pk2)
        setattr(entity_1, self.relationship_name, entity_2)
        await entity_crud.session_manager.commit_and_refresh(
            session=session, object=entity_1
        )

    def create_relation(self, entity_crud: CrudForgery):
        async def endpoint(
            pk1: Any,
            pk2: Any,
            session: ElrahSession = Depends(self.yield_session),
        ):
            return await self.create_relation_crud(
                pk1=pk1, pk2=pk2, session=session, entity_crud=entity_crud
            )

        return endpoint

    def delete_relation(self, entity_crud: CrudForgery):
        async def endpoint(
            pk1: Any, session: ElrahSession = Depends(self.yield_session)
        ):
            entity_1 = await entity_crud.read_one(session=session, pk=pk1)
            setattr(entity_1, self.relationship_name, None)
            await entity_crud.session_manager.commit_and_refresh(
                session=session, object=entity_1
            )

        return endpoint

    def create_by_relation(
        self,
        entity_crud: CrudForgery,
    ):
        async def endpoint(
            pk1: Any,
            create_obj: self.second_entity_crud.CreatePydanticModel,
            session: ElrahSession = Depends(self.yield_session),
        ):
            e1 = await entity_crud.read_one(session=session, pk=pk1)
            e2 = getattr(e1, self.relationship_name)
            if e2 is not None:
                detail = f"{self.second_entity_crud.entity_name} already exists for {entity_crud.entity_name} with pk {pk1}"
                raise_custom_http_exception(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=detail
                )
            new_obj = await self.second_entity_crud.create(
                session=session, create_obj=create_obj
            )
            pk2 = getattr(new_obj, self.second_entity_crud.primary_key_name)
            await self.create_relation_crud(
                session=session, entity_crud=entity_crud, pk1=pk1, pk2=pk2
            )
            return new_obj

        return endpoint

    def delete_by_relation(self, entity_crud: CrudForgery):
        async def endpoint(
            pk1: Any,
            session: ElrahSession = Depends(self.yield_session),
        ):
            entity_1 = await entity_crud.read_one(session=session, pk=pk1)
            entity_2 = getattr(entity_1, self.relationship_name)
            e2_pk = getattr(entity_2, self.second_entity_crud.primary_key_name)
            entity_2 = None
            return await self.second_entity_crud.delete(session=session, pk=e2_pk)

        return endpoint

    def soft_delete_by_relation(self, entity_crud: CrudForgery):
        async def endpoint(
            pk1: Any,
            session: ElrahSession = Depends(self.yield_session),
        ):
            entity_1 = await entity_crud.read_one(session=session, pk=pk1)
            entity_2 = getattr(entity_1, self.relationship_name)
            e2_pk = getattr(entity_2, self.second_entity_crud.primary_key_name)
            entity_2 = None
            return await self.second_entity_crud.soft_delete(session=session, pk=e2_pk)

        return endpoint

    def read_one_by_relation(self, entity_crud: CrudForgery):
        async def endpoint(
            pk1: Any,
            with_deleted: bool | None = None,
            session: ElrahSession = Depends(self.yield_session),
        ):
            e1 = await entity_crud.read_one(
                session=session, pk=pk1, with_deleted=with_deleted
            )
            e2 = getattr(e1, self.relationship_name)
            e2_is_deleted = getattr(e2, "is_deleted")
            if e2 is None or (e2_is_deleted and not with_deleted):
                detail = f"{self.relationship_name} not found for {entity_crud.entity_name} with pk {pk1}"
                raise_custom_http_exception(
                    status_code=status.HTTP_404_NOT_FOUND, detail=detail
                )
            return e2

        return endpoint

    def update_by_relation(
        self,
        entity_crud: CrudForgery,
    ):
        async def endpoint(
            pk1: Any,
            update_obj: self.second_entity_crud.UpdatePydanticModel,
            session: ElrahSession = Depends(self.yield_session),
        ):
            entity_1 = await entity_crud.read_one(session=session, pk=pk1)
            entity_2 = getattr(entity_1, self.relationship_name)
            pk2 = getattr(entity_2, self.second_entity_crud.primary_key_name)
            entity_2 = await self.second_entity_crud.update(
                session=session, pk=pk2, update_obj=update_obj, is_full_update=True
            )
            await entity_crud.session_manager.commit_and_refresh(
                session=session, object=entity_1
            )
            return entity_2

        return endpoint

    def patch_by_relation(
        self,
        entity_crud: CrudForgery,
    ):
        async def endpoint(
            pk1: Any,
            update_obj: self.second_entity_crud.PatchPydanticModel,
            session: ElrahSession = Depends(self.yield_session),
        ):
            entity_1 = await entity_crud.read_one(session=session, pk=pk1)
            entity_2 = getattr(entity_1, self.relationship_name)
            pk2 = getattr(entity_2, self.second_entity_crud.primary_key_name)
            entity_2 = await self.second_entity_crud.update(
                session=session, pk=pk2, update_obj=update_obj, is_full_update=False
            )
            await entity_crud.session_manager.commit_and_refresh(
                session=session, object=entity_1
            )
            return entity_2

        return endpoint
