from fastapi import APIRouter,Depends
from harlequelrah_fastapi.authentication.authenticate import Authentication
from typing import List, Optional
from harlequelrah_fastapi.crud.crud_model import CrudForgery
from harlequelrah_fastapi.router.route_config import RouteConfig


class CustomRouterProvider:
    ROUTES_NAME : List[str]=[
        "count",
        "read-one",
        "read-all",
        "read-all-by-filter",
        "create",
        "update",
        "delete",
    ]
    DEFAULT_CONFIG : List[RouteConfig]=[RouteConfig(route_name,is_activated=True,is_protected=False) for route_name in ROUTES_NAME]
    AUTH_CONFIG : List[RouteConfig]=[RouteConfig(route_name,is_activated=True,is_protected=True) for route_name in ROUTES_NAME]
    def __init__(
        self,
        prefix: str,
        tags: List[str],
        PydanticModel,
        crud: CrudForgery,
        get_access_token: Optional[callable] = None,
        get_session: callable = None,
    ):
        self.crud = crud
        self.token_dependency = [
            Depends(get_access_token) if get_access_token else Depends(None)
        ]
        self.get_access_token : callable = get_access_token
        self.PydanticModel = PydanticModel
        self.CreatePydanticModel = crud.CreatePydanticModel
        self.UpdatePydanticModel = crud.UpdatePydanticModel
        self.router = APIRouter(
            prefix=prefix,
            tags=tags,
            dependencies= [
                    Depends(get_session),
                ]
            ,
        )

    def get_default_router(self):
        return self.initialize_router(init_data=self.DEFAULT_CONFIG)


    def get_protected_router(self):
        return self.initialize_router(init_data=self.AUTH_CONFIG)

    def initialize_router(self, init_data: List[RouteConfig]):
        for config in init_data:
            if config.route_name ==  "count" and config.is_activated:

                @self.router.get(
                    f"/count",
                    dependencies=[Depends(self.get_access_token) ]if self.get_access_token and config.is_protected else []
                )
                async def count():
                    count = await self.crud.count()
                    return {"count": count}

            if config.route_name ==  "read-one" and config.is_activated:
                @self.router.get(
                    "/read-one/{id}",
                    response_model=self.PydanticModel,
                    dependencies=[Depends(self.get_access_token) ]if self.get_access_token and config.is_protected else []

                )
                async def read_one(
                    id: int,
                ):
                    return await self.crud.read_one(id)

            if config.route_name=="read-all" and config.is_activated:

                @self.router.get(
                    "/read-all",
                    response_model=List[self.PydanticModel],
                    dependencies=[Depends(self.get_access_token) ]if self.get_access_token and config.is_protected else []
                )
                async def read_all(
                    skip: int = 0,
                    limit: int = None
                ):
                    return await self.crud.read_all(skip=skip, limit=limit)

            if config.route_name == "read-all-by-filter" and config.is_activated:

                @self.router.get(
                    "/read-all-by-filter",
                    response_model=List[self.PydanticModel],
                    dependencies=[Depends(self.get_access_token) ]if self.get_access_token and config.is_protected else []
                )
                async def read_all_by_filter(
                    filter: str,
                    value: str,
                    skip: int = 0,
                    limit: int = None,
                ):
                    return await self.crud.read_all_by_filter(
                        skip=skip, limit=limit, filter=filter, value=value
                    )

            if config.route_name == "create" and config.is_activated:

                @self.router.post(
                    "/create",
                    response_model=self.PydanticModel,
                    dependencies=[Depends(self.get_access_token) ]if self.get_access_token and config.is_protected else [],
                )
                async def create(
                    create_obj: self.CreatePydanticModel,
                ):
                    return await self.crud.create(create_obj)

            if config.route_name=="update" and config.is_activated:

                @self.router.put(
                    "/update/{id}",
                    response_model=self.PydanticModel,
                    dependencies=[Depends(self.get_access_token) ]if self.get_access_token and config.is_protected else [],
                )
                async def update(
                    id: int,
                    update_obj: self.UpdatePydanticModel,
                ):
                    return await self.crud.update(id, update_obj)

            if  config.route_name=="delete" and config.is_activated:

                @self.router.delete("/delete/{id}", dependencies=[Depends(self.get_access_token) ]if self.get_access_token and config.is_protected else [])
                async def delete(
                    id: int,
                ):
                    return await self.crud.delete(id)
        return self.router
