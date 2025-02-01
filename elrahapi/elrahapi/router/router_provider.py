from fastapi import APIRouter

from typing import List, Optional
from elrahapi.crud.crud_forgery import CrudForgery
from elrahapi.router.route_config import AuthorizationConfig, RouteConfig
from elrahapi.router.router_crud import add_authorizations, exclude_route, format_init_data, get_single_route, initialize_dependecies
from elrahapi.router.router_namespace import (
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
        roles : Optional[List[str]]= None,
        privileges : Optional[List[str]]=None
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
        init_data: Optional[List[RouteConfig]] = None,
        public_routes_name: Optional[List[DefaultRoutesName]] =None,
        protected_routes_name: Optional[List[DefaultRoutesName]] =None,
        exclude_routes_name: Optional[List[DefaultRoutesName]] = None,
    ) -> APIRouter:
        if init_data is None: init_data=[]
        if public_routes_name :
            for route_name in public_routes_name:
                route = get_single_route(route_name)
                init_data.append(route)
        if protected_routes_name:
            for route_name in protected_routes_name:
                route = get_single_route(route_name, TypeRoute.PROTECTED)
                init_data.append(route)
        custom_init_data = exclude_route(init_data, exclude_routes_name)
        return self.initialize_router(custom_init_data)

    def get_protected_router(
        self, authorizations:Optional[List[AuthorizationConfig]]=None, exclude_routes_name: Optional[List[DefaultRoutesName]] = None
    ) -> APIRouter:
        return self.initialize_router(
            init_data=ROUTES_PROTECTED_CONFIG,
            exclude_routes_name=exclude_routes_name,
            authorizations=authorizations
            )

    def initialize_router(
        self,
        init_data: List[RouteConfig],
        authorizations:Optional[List[AuthorizationConfig]]=None,
        exclude_routes_name: Optional[List[DefaultRoutesName]] = None,
    ) -> APIRouter:
        init_data = format_init_data(init_data=init_data, authorizations=authorizations,exclude_routes_name=exclude_routes_name)
        for config in init_data:
            if config.route_name == DefaultRoutesName.COUNT and config.is_activated:
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
                config.route_name == DefaultRoutesName.READ_ONE
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

            if config.route_name == DefaultRoutesName.READ_ALL_BY_FILTER and config.is_activated:
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

            if config.route_name == DefaultRoutesName.CREATE and config.is_activated:
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

            if config.route_name == DefaultRoutesName.UPDATE and config.is_activated:
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
