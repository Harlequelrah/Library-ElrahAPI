from fastapi import APIRouter

from typing import List, Optional
from harlequelrah_fastapi.crud.crud_forgery import CrudForgery
from harlequelrah_fastapi.router.route_config import RouteConfig
from harlequelrah_fastapi.router.router_crud import exclude_route, get_single_route, initialize_dependecies
from harlequelrah_fastapi.router.router_namespace import (
    DefaultRoutesName,
    ROUTES_PROTECTED_CONFIG,
    ROUTES_PUBLIC_CONFIG,
    TypeRoute,
)


class CustomRouterProvider:

    def __init__(
        self,
        prefix: str,
        tags: List[str],
        PydanticModel,
        crud: CrudForgery,
        roles : Optional[List[str]]= [],
        privileges : Optional[List[str]]=[]
    ):
        self.crud = crud
        self.get_access_token: callable = crud.authentication.get_access_token
        self.session_factory:callable=crud.authentication.session_factory
        self.PydanticModel = PydanticModel
        self.CreatePydanticModel = crud.CreatePydanticModel
        self.UpdatePydanticModel = crud.UpdatePydanticModel
        self.roles= roles
        self.privileges = privileges
        self.router = APIRouter(
            prefix=prefix,
            tags=tags,
        )





    def get_public_router(
        self, exclude_routes_name: Optional[List[DefaultRoutesName]] = None
    ) -> APIRouter:
        return self.initialize_router(ROUTES_PUBLIC_CONFIG, exclude_routes_name)

    def get_mixed_router(
        self,
        init_data: List[RouteConfig] = [],
        public_routes_name: Optional[List[DefaultRoutesName]] = [],
        protected_routes_name: Optional[List[DefaultRoutesName]] = [],
        exclude_routes_name: Optional[List[DefaultRoutesName]] = None,
    ) -> APIRouter:
        for route_name in public_routes_name:
            route = get_single_route(route_name)
            init_data.append(route)
        for route_name in protected_routes_name:
            route = get_single_route(route_name, TypeRoute.PROTECTED)
            init_data.append(route)
        custom_init_data = exclude_route(init_data, exclude_routes_name)
        return self.initialize_router(custom_init_data)

    def get_protected_router(
        self, exclude_routes_name: Optional[List[DefaultRoutesName]] = None
    ) -> APIRouter:
        return self.initialize_router(ROUTES_PROTECTED_CONFIG, exclude_routes_name)

    def initialize_router(
        self,
        init_data: List[RouteConfig],
        exclude_routes_name: Optional[List[DefaultRoutesName]] = None,
    ) -> APIRouter:
        init_data = exclude_route(init_data, exclude_routes_name)
        for config in init_data:
            if config.route_name == DefaultRoutesName.COUNT.value and config.is_activated:
                dependencies= initialize_dependecies(
                    config=config,
                    authentication= self.crud.authentication,
                    roles=self.roles,
                    privileges = self.privileges
                )
                @self.router.get(
                    path=config.route_path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    dependencies = dependencies
                )
                async def count():
                    count = await self.crud.count()
                    return {"count": count}

            if (
                config.route_name == DefaultRoutesName.READ_ONE.value
                and config.is_activated
            ):
                dependencies= initialize_dependecies(
                    config=config,
                    authentication= self.crud.authentication,
                    roles=self.roles,
                    privileges = self.privileges
                )

                @self.router.get(
                    path=config.route_path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    response_model=self.PydanticModel,
                    dependencies = dependencies
                )
                async def read_one(
                    id: int,
                ):
                    return await self.crud.read_one(id)

            if config.route_name == DefaultRoutesName.READ_ALL and config.is_activated:
                dependencies= initialize_dependecies(
                    config=config,
                    authentication= self.crud.authentication,
                    roles=self.roles,
                    privileges = self.privileges
                )

                @self.router.get(
                    path=config.route_path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    response_model=List[self.PydanticModel],
                    dependencies = dependencies
                )
                async def read_all(skip: int = 0, limit: int = None):
                    return await self.crud.read_all(skip=skip, limit=limit)

            if config.route_name == DefaultRoutesName.READ_ALL_BY_FILTER.value and config.is_activated:
                dependencies= initialize_dependecies(
                    config=config,
                    authentication= self.crud.authentication,
                    roles=self.roles,
                    privileges = self.privileges
                )

                @self.router.get(
                    path=config.route_path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    response_model=List[self.PydanticModel],
                    dependencies = dependencies
                )
                async def read_all_by_filter(
                    filter,
                    value,
                    skip: int = 0,
                    limit: int = None,
                ):
                    return await self.crud.read_all_by_filter(
                        skip=skip, limit=limit, filter=filter, value=value
                    )

            if config.route_name == DefaultRoutesName.CREATE.value and config.is_activated:
                dependencies= initialize_dependecies(
                    config=config,
                    authentication= self.crud.authentication,
                    roles=self.roles,
                    privileges = self.privileges
                )

                @self.router.post(
                    path=config.route_path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    response_model=self.PydanticModel,
                    dependencies = dependencies
                )
                async def create(
                    create_obj: self.CreatePydanticModel,
                ):
                    return await self.crud.create(create_obj)

            if config.route_name == DefaultRoutesName.UPDATE.value and config.is_activated:
                dependencies= initialize_dependecies(
                    config=config,
                    authentication= self.crud.authentication,
                    roles=self.roles,
                    privileges = self.privileges
                )

                @self.router.put(
                    path=config.route_path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    response_model=self.PydanticModel,
                    dependencies = dependencies
                )
                async def update(
                    id: int,
                    update_obj: self.UpdatePydanticModel,
                ):
                    return await self.crud.update(id, update_obj)

            if config.route_name == DefaultRoutesName.DELETE.value and config.is_activated:
                dependencies= initialize_dependecies(
                    config=config,
                    authentication= self.crud.authentication,
                    roles=self.roles,
                    privileges = self.privileges
                )

                @self.router.delete(
                    path=config.route_path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    dependencies = dependencies,
                    status_code=204,
                )
                async def delete(
                    id: int,
                ):
                    return await self.crud.delete(id)

        return self.router
