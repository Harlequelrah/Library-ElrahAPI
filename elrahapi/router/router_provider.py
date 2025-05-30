from copy import deepcopy
from typing import Any, List, Optional

from elrahapi.authentication.authentication_manager import AuthenticationManager
from elrahapi.crud.bulk_models import BulkDeleteModel
from elrahapi.crud.crud_forgery import CrudForgery
from elrahapi.router.relationship import Relationship
from elrahapi.router.route_config import (
    AuthorizationConfig,
    ResponseModelConfig,
    RouteConfig,
)
from elrahapi.router.router_crud import (
    format_init_data,
    get_single_route,
    is_verified_relation_rule,
)
from elrahapi.router.router_namespace import (
    ROUTES_PROTECTED_CONFIG,
    ROUTES_PUBLIC_CONFIG,
    DefaultRoutesName,
    RelationRoutesName,
    TypeRelation,
    TypeRoute,
)
from elrahapi.utility.types import ElrahSession

from fastapi import APIRouter, Depends, status


class CustomRouterProvider:

    def __init__(
        self,
        prefix: str,
        tags: List[str],
        crud: CrudForgery,
        roles: Optional[List[str]] = None,
        privileges: Optional[List[str]] = None,
        authentication: Optional[AuthenticationManager] = None,
        read_with_relations: bool = False,
        relations: Optional[List[Relationship]] = None,
    ):
        self.relations = relations or []
        self.authentication: AuthenticationManager = (
            authentication if authentication else None
        )
        self.get_access_token: Optional[callable] = (
            authentication.get_access_token if authentication else None
        )
        self.read_with_relations = read_with_relations
        self.ReadPydanticModel = crud.ReadPydanticModel
        self.FullReadPydanticModel = crud.FullReadPydanticModel
        self.CreatePydanticModel = crud.CreatePydanticModel
        self.UpdatePydanticModel = crud.UpdatePydanticModel
        self.PatchPydanticModel = crud.PatchPydanticModel
        self.crud = crud
        self.roles = roles
        self.privileges = privileges
        self.router = APIRouter(
            prefix=prefix,
            tags=tags,
        )

    def get_public_router(
        self,
        exclude_routes_name: Optional[List[DefaultRoutesName]] = None,
        response_model_configs: Optional[List[ResponseModelConfig]] = None,
    ) -> APIRouter:
        return self.initialize_router(
            init_data=ROUTES_PUBLIC_CONFIG,
            exclude_routes_name=exclude_routes_name,
            response_model_configs=response_model_configs,
        )

    def get_protected_router(
        self,
        authorizations: Optional[List[AuthorizationConfig]] = None,
        exclude_routes_name: Optional[List[DefaultRoutesName]] = None,
        response_model_configs: Optional[List[ResponseModelConfig]] = None,
    ) -> APIRouter:
        if not self.authentication:
            raise ValueError("No authentication provided in the router provider")
        return self.initialize_router(
            init_data=ROUTES_PROTECTED_CONFIG,
            exclude_routes_name=exclude_routes_name,
            authorizations=authorizations,
            response_model_configs=response_model_configs,
        )

    def get_custom_router_init_data(
        self,
        is_protected: TypeRoute,
        init_data: Optional[List[RouteConfig]] = None,
        route_names: Optional[List[DefaultRoutesName]] = None,
    ):
        custom_init_data = init_data if init_data else []
        if route_names:
            for route_name in route_names:
                if is_protected == TypeRoute.PROTECTED and not self.authentication:
                    raise ValueError(
                        "No authentication provided in the router provider"
                    )
                route = get_single_route(route_name, is_protected)
                custom_init_data.append(route)
        return custom_init_data

    def get_custom_router(
        self,
        init_data: Optional[List[RouteConfig]] = None,
        routes_name: Optional[List[DefaultRoutesName]] = None,
        exclude_routes_name: Optional[List[DefaultRoutesName]] = None,
        authorizations: Optional[List[AuthorizationConfig]] = None,
        response_model_configs: Optional[List[ResponseModelConfig]] = None,
        type_route: TypeRoute = TypeRoute.PUBLIC,
    ):
        if type_route == TypeRoute.PROTECTED and not self.authentication:
            raise ValueError("No authentication provided in the router provider")
        custom_init_data = self.get_custom_router_init_data(
            init_data=init_data, route_names=routes_name, is_protected=type_route
        )
        return self.initialize_router(
            custom_init_data,
            exclude_routes_name=exclude_routes_name,
            authorizations=authorizations,
            response_model_configs=response_model_configs,
        )

    def get_mixed_router(
        self,
        init_data: Optional[List[RouteConfig]] = None,
        public_routes_name: Optional[List[DefaultRoutesName]] = None,
        protected_routes_name: Optional[List[DefaultRoutesName]] = None,
        exclude_routes_name: Optional[List[DefaultRoutesName]] = None,
        response_model_configs: Optional[List[ResponseModelConfig]] = None,
    ) -> APIRouter:
        if not self.authentication:
            raise ValueError("No authentication provided in the router provider")
        if init_data is None:
            init_data = []
        public_routes_data = self.get_custom_router_init_data(
            init_data=init_data,
            route_names=public_routes_name,
            is_protected=TypeRoute.PUBLIC,
        )
        protected_routes_data = self.get_custom_router_init_data(
            init_data=init_data,
            route_names=protected_routes_name,
            is_protected=TypeRoute.PROTECTED,
        )
        custom_init_data = public_routes_data + protected_routes_data
        return self.initialize_router(
            init_data=custom_init_data,
            exclude_routes_name=exclude_routes_name,
            response_model_configs=response_model_configs,
        )

    def initialize_router(
        self,
        init_data: List[RouteConfig],
        authorizations: Optional[List[AuthorizationConfig]] = None,
        exclude_routes_name: Optional[List[DefaultRoutesName]] = None,
        response_model_configs: Optional[List[ResponseModelConfig]] = None,
    ) -> APIRouter:
        copied_init_data = deepcopy(init_data)
        formatted_data = format_init_data(
            init_data=copied_init_data,
            authorizations=authorizations,
            exclude_routes_name=exclude_routes_name,
            authentication=self.authentication,
            roles=self.roles,
            privileges=self.privileges,
            response_model_configs=response_model_configs,
            read_with_relations=self.read_with_relations,
            ReadPydanticModel=self.ReadPydanticModel,
            FullReadPydanticModel=self.FullReadPydanticModel,
        )

        for config in formatted_data:
            if config.route_name == DefaultRoutesName.COUNT:

                @self.router.get(
                    path=config.route_path,
                    summary=config.summary,
                    description=config.description,
                    dependencies=config.dependencies,
                    operation_id=f"{config.route_name}_{self.crud.entity_name}",
                    name=f"{config.route_name}_{self.crud.entity_name}",
                )
                async def count(
                    session: ElrahSession = Depends(self.crud.session_manager.yield_session)
                ):
                    count = await self.crud.count(session=session)
                    return {"count": count}

            if config.route_name == DefaultRoutesName.READ_ONE:

                @self.router.get(
                    path=config.route_path,
                    summary=config.summary,
                    description=config.description,
                    response_model=config.response_model,
                    dependencies=config.dependencies,
                    operation_id=f"{config.route_name}_{self.crud.entity_name}",
                    name=f"{config.route_name}_{self.crud.entity_name}",
                )
                async def read_one(
                    pk: Any,
                    session: ElrahSession = Depends(
                        self.crud.session_manager.yield_session
                    ),
                ):
                    return await self.crud.read_one(
                        session=session,
                        pk=pk
                        )

            if config.route_name == DefaultRoutesName.READ_ALL:

                @self.router.get(
                    path=config.route_path,
                    summary=config.summary,
                    description=config.description,
                    response_model=List[config.response_model],
                    dependencies=config.dependencies,
                    operation_id=f"{config.route_name}_{self.crud.entity_name}",
                    name=f"{config.route_name}_{self.crud.entity_name}",
                )
                async def read_all(
                    filter: Optional[str] = None,
                    value: Optional[Any] = None,
                    second_model_filter: Optional[str] = None,
                    second_model_filter_value: Optional[Any] = None,
                    skip: int = None,
                    limit: int = None,
                    relationship_name: Optional[str] = None,
                    session: ElrahSession = Depends(
                        self.crud.session_manager.yield_session
                    ),
                ):
                    relation: Optional[Relationship] = self.get_relationship(
                        relationship_name=relationship_name
                    )
                    return await self.crud.read_all(
                        skip=skip,
                        limit=limit,
                        filter=filter,
                        value=value,
                        second_model_filter=second_model_filter,
                        second_model_filter_value=second_model_filter_value,
                        relation=relation,
                        session=session
                    )

            if (
                config.route_name == DefaultRoutesName.CREATE
                and self.CreatePydanticModel
            ):

                @self.router.post(
                    path=config.route_path,
                    summary=config.summary,
                    description=config.description,
                    response_model=config.response_model,
                    dependencies=config.dependencies,
                    status_code=status.HTTP_201_CREATED,
                    operation_id=f"{config.route_name}_{self.crud.entity_name}",
                    name=f"{config.route_name}_{self.crud.entity_name}",
                )
                async def create(
                    create_obj: self.CreatePydanticModel,
                    session: ElrahSession = Depends(
                        self.crud.session_manager.yield_session
                    ),
                ):
                    return await self.crud.create(
                        session=session,
                        create_obj=create_obj
                    )

            if (
                config.route_name == DefaultRoutesName.UPDATE
                and self.UpdatePydanticModel
            ):

                @self.router.put(
                    path=config.route_path,
                    summary=config.summary,
                    description=config.description,
                    response_model=config.response_model,
                    dependencies=config.dependencies,
                    operation_id=f"{config.route_name}_{self.crud.entity_name}",
                    name=f"{config.route_name}_{self.crud.entity_name}",
                )
                async def update(
                    pk: Any,
                    update_obj: self.UpdatePydanticModel,
                    session: ElrahSession = Depends(
                        self.crud.session_manager.yield_session
                    ),
                ):
                    return await self.crud.update(
                        pk=pk,
                        update_obj=update_obj,
                        is_full_update=True,
                        session=session,
                    )

            if config.route_name == DefaultRoutesName.PATCH and self.PatchPydanticModel:

                @self.router.patch(
                    path=config.route_path,
                    summary=config.summary,
                    description=config.description,
                    response_model=config.response_model,
                    dependencies=config.dependencies,
                    operation_id=f"{config.route_name}_{self.crud.entity_name}",
                    name=f"{config.route_name}_{self.crud.entity_name}",
                )
                async def patch(
                    pk: Any,
                    update_obj: self.PatchPydanticModel,
                    session: ElrahSession = Depends(
                        self.crud.session_manager.yield_session
                    ),
                ):
                    return await self.crud.update(
                        pk=pk,
                        update_obj=update_obj,
                        is_full_update=False,
                        session=session
                    )

            if config.route_name == DefaultRoutesName.DELETE:

                @self.router.delete(
                    path=config.route_path,
                    summary=config.summary,
                    description=config.description,
                    dependencies=config.dependencies,
                    status_code=status.HTTP_204_NO_CONTENT,
                    operation_id=f"{config.route_name}_{self.crud.entity_name}",
                    name=f"{config.route_name}_{self.crud.entity_name}",
                )
                async def delete(
                    pk: Any,
                    session: ElrahSession = Depends(
                        self.crud.session_manager.yield_session
                    ),
                ):
                    return await self.crud.delete(
                        session=session,
                        pk=pk
                        )

            if config.route_name == DefaultRoutesName.BULK_DELETE:

                @self.router.delete(
                    path=config.route_path,
                    summary=config.summary,
                    description=config.description,
                    dependencies=config.dependencies,
                    status_code=status.HTTP_204_NO_CONTENT,
                    operation_id=f"{config.route_name}_{self.crud.entity_name}",
                    name=f"{config.route_name}_{self.crud.entity_name}",
                )
                async def bulk_delete(
                    pk_list: BulkDeleteModel,
                    session: ElrahSession = Depends(
                        self.crud.session_manager.yield_session
                    ),
                ):
                    return await self.crud.bulk_delete(
                        session=session,
                        pk_list=pk_list
                        )

            if config.route_name == DefaultRoutesName.BULK_CREATE:

                @self.router.post(
                    path=config.route_path,
                    summary=config.summary,
                    description=config.description,
                    dependencies=config.dependencies,
                    response_model=List[config.response_model],
                    status_code=status.HTTP_201_CREATED,
                    operation_id=f"{config.route_name}_{self.crud.entity_name}",
                    name=f"{config.route_name}_{self.crud.entity_name}",
                )
                async def bulk_create(
                    create_obj_list: List[self.CreatePydanticModel],
                    session: ElrahSession = Depends(
                        self.crud.session_manager.yield_session
                    ),
                ):
                    return await self.crud.bulk_create(
                        session=session,
                        create_obj_list=create_obj_list
                    )

        for relation in self.relations:
            routes_configs = relation.init_routes_configs(
                roles=self.roles,
                privileges=self.privileges,
                authentication=self.authentication,
            )
            for route_config in routes_configs:
                if (
                    route_config.route_name == RelationRoutesName.CREATE_RELATION
                    and is_verified_relation_rule(
                        type_relation=relation.type_relation,
                        relation_route_name=route_config.route_name
                    )
                ):
                    self.router.add_api_route(
                        path=route_config.route_path,
                        endpoint=self.make_create_relation_route(relation=relation),
                        methods=["POST"],
                        dependencies=route_config.dependencies,
                        summary=route_config.summary,
                        description=route_config.description,
                        response_model=route_config.response_model,
                        status_code=status.HTTP_201_CREATED,
                        operation_id=f"{relation.relationship_name}_{route_config.route_name}_{self.crud.entity_name}",
                        name=f"{relation.relationship_name}_{route_config.route_name}_{self.crud.entity_name}",
                    )
                if (
                    route_config.route_name == RelationRoutesName.DELETE_RELATION
                    and is_verified_relation_rule(
                        type_relation=relation.type_relation,
                        relation_route_name=route_config.route_name,
                    )
                ):
                    self.router.add_api_route(
                        endpoint=self.make_delete_relation_route(relation=relation),
                        methods=["DELETE"],
                        path=route_config.route_path,
                        dependencies=route_config.dependencies,
                        status_code=status.HTTP_204_NO_CONTENT,
                        summary=route_config.summary,
                        description=route_config.description,
                        operation_id=f"{relation.relationship_name}_{route_config.route_name}_{self.crud.entity_name}",
                        name=f"{relation.relationship_name}_{route_config.route_name}_{self.crud.entity_name}",
                    )
                if (
                    route_config.route_name == RelationRoutesName.READ_ALL_BY_RELATION
                    and is_verified_relation_rule(
                        type_relation=relation.type_relation,
                        relation_route_name=route_config.route_name,
                    )
                ):
                    self.router.add_api_route(
                        endpoint=self.make_read_all_by_relation_route(relation=relation),
                        methods=["GET"],
                        path=route_config.route_path,
                        dependencies=route_config.dependencies,
                        response_model=List[route_config.response_model],
                        summary=route_config.summary,
                        description=route_config.description,
                        operation_id=f"{relation.relationship_name}_{route_config.route_name}_{self.crud.entity_name}",
                        name=f"{relation.relationship_name}_{route_config.route_name}_{self.crud.entity_name}",
                    )
                if (
                    route_config.route_name == RelationRoutesName.READ_ONE_BY_RELATION
                    and is_verified_relation_rule(
                        type_relation=relation.type_relation,
                        relation_route_name=route_config.route_name,
                    )
                ):
                    self.router.add_api_route(
                        endpoint=self.make_read_one_by_relation_route(relation=relation),
                        methods=["GET"],
                        path=route_config.route_path,
                        dependencies=route_config.dependencies,
                        response_model=route_config.response_model,
                        summary=route_config.summary,
                        description=route_config.description,
                        operation_id=f"{relation.relationship_name}_{route_config.route_name}_{self.crud.entity_name}",
                        name=f"{relation.relationship_name}_{route_config.route_name}_{self.crud.entity_name}",
                    )
                if (
                    route_config.route_name == RelationRoutesName.CREATE_BY_RELATION
                    and is_verified_relation_rule(
                        type_relation=relation.type_relation,
                        relation_route_name=route_config.route_name,
                    )
                ):
                    self.router.add_api_route(
                        endpoint=self.make_create_by_relation_route(relation=relation),
                        methods=["POST"],
                        path=route_config.route_path,
                        dependencies=route_config.dependencies,
                        response_model=route_config.response_model,
                        summary=route_config.summary,
                        description=route_config.description,
                        status_code=status.HTTP_201_CREATED,
                        operation_id=f"{relation.relationship_name}_{route_config.route_name}_{self.crud.entity_name}",
                        name=f"{relation.relationship_name}_{route_config.route_name}_{self.crud.entity_name}",
                    )

                if (
                    route_config.route_name == RelationRoutesName.DELETE_BY_RELATION
                    and is_verified_relation_rule(
                        type_relation=relation.type_relation,
                        relation_route_name=route_config.route_name,
                    )
                ):
                    self.router.add_api_route(
                        endpoint=self.make_delete_by_relation_route(relation=relation),
                        methods=["DELETE"],
                        path=route_config.route_path,
                        dependencies=route_config.dependencies,
                        status_code=status.HTTP_204_NO_CONTENT,
                        summary=route_config.summary,
                        description=route_config.description,
                        operation_id=f"{relation.relationship_name}_{route_config.route_name}_{self.crud.entity_name}",
                        name=f"{relation.relationship_name}_{route_config.route_name}_{self.crud.entity_name}",
                    )

                if (
                    route_config.route_name == RelationRoutesName.UPDATE_BY_RELATION
                    and is_verified_relation_rule(
                        type_relation=relation.type_relation,
                        relation_route_name=route_config.route_name,
                    )
                ):
                    self.router.add_api_route(
                        endpoint=self.make_update_by_relation_route(relation=relation),
                        methods=["PUT"],
                        path=route_config.route_path,
                        dependencies=route_config.dependencies,
                        response_model=route_config.response_model,
                        summary=route_config.summary,
                        description=route_config.description,
                        operation_id=f"{relation.relationship_name}_{route_config.route_name}_{self.crud.entity_name}",
                        name=f"{relation.relationship_name}_{route_config.route_name}_{self.crud.entity_name}",
                    )

                if (
                    route_config.route_name == RelationRoutesName.PATCH_BY_RELATION
                    and is_verified_relation_rule(
                        type_relation=relation.type_relation,
                        relation_route_name=route_config.route_name,
                    )
                ):
                    self.router.add_api_route(
                        endpoint=self.make_patch_by_relation_route(relation=relation),
                        methods=["PATCH"],
                        path=route_config.route_path,
                        dependencies=route_config.dependencies,
                        response_model=route_config.response_model,
                        summary=route_config.summary,
                        description=route_config.description,
                        operation_id=f"{relation.relationship_name}_{route_config.route_name}_{self.crud.entity_name}",
                        name=f"{relation.relationship_name}_{route_config.route_name}_{self.crud.entity_name}",
                    )

        return self.router

    def get_relationship(self, relationship_name: str):
        relation: Optional[Relationship] = next(
            (
                relation
                for relation in self.relations
                if relation.relationship_name == relationship_name
            ),
            None,
        )
        if relation and relation.type_relation not in [
            TypeRelation.MANY_TO_MANY_CLASS,
            TypeRelation.MANY_TO_MANY_TABLE,
            TypeRelation.ONE_TO_MANY,
        ]:
            relation = None
        return relation

    def make_create_relation_route(
        self,
        relation:Relationship,
        ):
        async def create_relation(
                pk1: Any,
                pk2: Any,
                session: ElrahSession = Depends(
                    self.crud.session_manager.yield_session
                    )
            ):
            return await relation.create_relation(
                    session=session,
                    entity_crud=self.crud,
                    pk1=pk1, pk2=pk2
                )
        return create_relation

    def make_delete_relation_route(self,relation:Relationship):
        async def delete_relation(
            pk1: Any,
            pk2: Any,
            session: ElrahSession = Depends(
            self.crud.session_manager.yield_session
                ),
            ):
            return await relation.delete_relation(
                    session=session,
                    entity_crud=self.crud,
                    pk1=pk1, pk2=pk2
                )
        return delete_relation

    def make_read_all_by_relation_route(self, relation: Relationship):
        async def read_all_by_relation(
            pk1: Any,
            filter: Optional[str] = None,
            value: Optional[Any] = None,
            skip: int = None,
            limit: int = None,
            session: ElrahSession = Depends(
                self.crud.session_manager.yield_session
            ),
            ):
            return await relation.read_all_by_relation(
                pk1=pk1,
                filter=filter,
                value=value,
                limit=limit,
                skip=skip,
                entity_crud=self.crud,
                session=session
            )
        return read_all_by_relation

    def make_read_one_by_relation_route(self, relation: Relationship):
        async def read_one_by_relation(
            pk1: Any,
            session: ElrahSession = Depends(
                self.crud.session_manager.yield_session
            ),
        ):
            return await relation.read_one_by_relation(
                session=session,
                entity_crud=self.crud,
                pk1=pk1
            )
        return read_one_by_relation

    def make_create_by_relation_route(self,relation: Relationship):

        async def create_by_relation(
            pk1: Any,
            create_obj: relation.second_entity_crud.crud_models.create_model,
            session: ElrahSession = Depends(self.crud.session_manager.yield_session),
        ):

            return await relation.create_by_relation(
                pk1=pk1, create_obj=create_obj, entity_crud=self.crud, session=session
            )
        return create_by_relation

    def make_delete_by_relation_route(self, relation: Relationship):
        async def delete_by_relation(
            pk1: Any,
            session: ElrahSession = Depends(self.crud.session_manager.yield_session),
        ):
            return await relation.delete_by_relation(
                pk1=pk1, entity_crud=self.crud, session=session
            )
        return delete_by_relation

    def make_update_by_relation_route(self, relation: Relationship):
        async def update_by_relation(
            pk1: Any,
            update_obj: relation.second_entity_crud.crud_models.update_model,
            session: ElrahSession = Depends(self.crud.session_manager.yield_session),
        ):
            return await relation.update_by_relation(
                pk1=pk1, update_obj=update_obj, entity_crud=self.crud, session=session
            )
        return update_by_relation
    def make_patch_by_relation_route(self, relation: Relationship):
        async def patch_by_relation(
            pk1: Any,
            patch_obj: relation.second_entity_crud.crud_models.patch_model,
            session: ElrahSession = Depends(self.crud.session_manager.yield_session),
        ):
            return await relation.patch_by_relation(
                pk1=pk1, patch_obj=patch_obj, entity_crud=self.crud, session=session
            )
        return patch_by_relation
