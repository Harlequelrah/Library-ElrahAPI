from typing import Any

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
from fastapi import Depends, status


class ManyToOneRelationship(BaseRelationship):
    RELATION_RULES = [RelationRoutesName.READ_ONE_BY_RELATION]

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

    def read_one_by_relation(self, entity_crud: CrudForgery):
        async def endpoint(
            pk1: Any, session: ElrahSession = Depends(self.yield_session),
            with_deleted:bool|None=None
        ):
            e1 = await entity_crud.read_one(session=session, pk=pk1,with_deleted=with_deleted)
            e2 = getattr(e1, self.relationship_name)
            if e2 is None:
                detail = f"{self.relationship_name} not found for {entity_crud.entity_name} with pk {pk1}"
                raise_custom_http_exception(
                    status_code=status.HTTP_404_NOT_FOUND, detail=detail
                )
            return e2

        return endpoint
