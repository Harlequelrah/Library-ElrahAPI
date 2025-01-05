from fastapi import APIRouter, Depends
from harlequelrah_fastapi.authentication.authenticate import Authentication
from typing import List, Optional
from harlequelrah_fastapi.crud.crud_model import CrudForgery
from harlequelrah_fastapi.router.route_config import RouteConfig
from harlequelrah_fastapi.router.router_crud import exclude_route, get_single_route
from harlequelrah_fastapi.router.router_namespace import  DEFAULTROUTESNAME, ROUTES_PROTECTED_CONFIG, ROUTES_PUBLIC_CONFIG


class CustomRouterProvider:

    def __init__(
        self,
        prefix: str,
        tags: List[str],
        PydanticModel,
        crud: CrudForgery ,
        get_access_token: Optional[callable] = None,
    ):
        self.crud = crud
        self.get_access_token: callable = get_access_token
        self.PydanticModel = PydanticModel
        self.CreatePydanticModel = crud.CreatePydanticModel
        self.UpdatePydanticModel = crud.UpdatePydanticModel
        self.router = APIRouter(
            prefix=prefix,
            tags=tags,
        )

    def get_public_router(
        self, exclude_routes_name: Optional[List[DEFAULTROUTESNAME]] = None
    ) -> APIRouter:
        return  self.initialize_router(ROUTES_PUBLIC_CONFIG, exclude_routes_name)

    def get_mixed_router(
        self,
        init_data: List[RouteConfig] = [],
        public_routes_name: Optional[List[DEFAULTROUTESNAME]] = None,
        protected_routes_name: Optional[List[DEFAULTROUTESNAME]] = None,
        exclude_routes_name: Optional[List[DEFAULTROUTESNAME]] = None,
    ) -> APIRouter:
        for route_name in public_routes_name:
            route=get_single_route(route_name)
            init_data.append(route)
        for route_name in protected_routes_name:
            route=get_single_route(route_name,"protected")
            init_data.append(route)
        custom_init_data=exclude_route(init_data,exclude_routes_name)
        return self.initialize_router(custom_init_data)

    def get_protected_router(self, exclude_routes_name: Optional[List[DEFAULTROUTESNAME]] = None) -> APIRouter:
        return self.initialize_router(ROUTES_PROTECTED_CONFIG, exclude_routes_name)

    def initialize_router(
        self,
        init_data: List[RouteConfig],
        exclude_routes_name: Optional[List[DEFAULTROUTESNAME]] = None,
    )->APIRouter:
        init_data = exclude_route(init_data, exclude_routes_name)
        for config in init_data:
            if config.route_name == "count" and config.is_activated:

                @self.router.get(
                    path=config.route_path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    dependencies=(
                        [Depends(self.get_access_token)]
                        if self.get_access_token and config.is_protected
                        else []
                    ),
                )
                async def count():
                    count = await self.crud.count()
                    return {"count": count}

            if config.route_name == "read-one" and config.is_activated and not config.is_unlocked:

                @self.router.get(
                    path=config.route_path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    response_model=self.PydanticModel,
                    dependencies=(
                        [Depends(self.get_access_token)]
                        if self.get_access_token and config.is_protected
                        else []
                    ),
                )
                async def read_one(
                    id: int,
                ):
                    return await self.crud.read_one(id)

            if config.route_name == "read-all" and config.is_activated:

                @self.router.get(
                    path=config.route_path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    response_model=List[self.PydanticModel],
                    dependencies=(
                        [Depends(self.get_access_token)]
                        if self.get_access_token and config.is_protected
                        else []
                    ),
                )
                async def read_all(skip: int = 0, limit: int = None):
                    return await self.crud.read_all(skip=skip, limit=limit)

            if config.route_name == "read-all-by-filter" and config.is_activated:

                @self.router.get(
                    path=config.route_path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    response_model=List[self.PydanticModel],
                    dependencies=(
                        [Depends(self.get_access_token)]
                        if self.get_access_token and config.is_protected
                        else []
                    ),
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

            if config.route_name == "create" and config.is_activated:

                @self.router.post(
                    path=config.route_path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    response_model=self.PydanticModel,
                    dependencies=(
                        [Depends(self.get_access_token)]
                        if self.get_access_token and config.is_protected
                        else []
                    ),
                )
                async def create(
                    create_obj: self.CreatePydanticModel,
                ):
                    return await self.crud.create(create_obj)

            if config.route_name == "update" and config.is_activated:

                @self.router.put(
                    path=config.route_path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    response_model=self.PydanticModel,
                    dependencies=(
                        [Depends(self.get_access_token)]
                        if self.get_access_token and config.is_protected
                        else []
                    ),
                )
                async def update(
                    id: int,
                    update_obj: self.UpdatePydanticModel,
                ):
                    return await self.crud.update(id, update_obj)

            if config.route_name == "delete" and config.is_activated:

                @self.router.delete(
                    path=config.route_path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    dependencies=(
                        [Depends(self.get_access_token)]
                        if self.get_access_token and config.is_protected
                        else []
                    ),
                    status_code=204
                )
                async def delete(
                    id: int,
                ):
                    return await self.crud.delete(id)
        return self.router
