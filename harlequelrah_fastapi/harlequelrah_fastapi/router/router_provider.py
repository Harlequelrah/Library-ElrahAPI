from fastapi import APIRouter,Depends
from harlequelrah_fastapi.authentication.authenticate import Authentication
from typing import List, Optional
from harlequelrah_fastapi.crud.crud_model import CrudForgery
from harlequelrah_fastapi.router.route_config import RouteConfig
def provide_router(prefix:str,tags:List[str],PydanticModel,crud:CrudForgery,authentication:Optional[Authentication]=None,get_session:Optional[callable]=None)->APIRouter:
    router = APIRouter(
        prefix=prefix,
        tags=tags,
        dependencies=[Depends(authentication.get_access_token),Depends(authentication.get_session)] if authentication else [Depends(get_session) if get_session else Depends()],
    )
    class UpdatePydanticModel(crud.UpdatePydanticModel):
        pass
    class CreatePydanticModel(crud.CreatePydanticModel):
        pass
    @router.get(f"/count")
    async def count():
        count= await crud.count()
        return {'count':count}

    @router.get("/read-one/{id}",response_model=PydanticModel)
    async def read_one(id:int):
        return await crud.read_one(id)

    @router.get("/read-all",response_model=List[PydanticModel])
    async def read_all(skip:int=0,limit:int=None):
        return await crud.read_all(skip=skip,limit=limit)

    @router.get("/read-all-by-filter",response_model=List[PydanticModel])
    async def read_all_by_filter(filter:str,value:str,skip:int=0,limit:int=None):
        return await crud.read_all_by_filter(skip=skip,limit=limit,filter=filter, value=value)

    @router.post("/create", response_model=PydanticModel)
    async def create(create_obj:CreatePydanticModel):
        return await crud.create(create_obj)

    @router.put("/update/{id}", response_model=PydanticModel)
    async def update(id:int,update_obj:UpdatePydanticModel):
        return await crud.update(id, update_obj)

    @router.delete("/delete/{id}")
    async def delete(id:int):
        return await crud.delete(id)

    return router

class ProvideRouter:
    def __init__(self,prefix:str,tags:List[str],PydanticModel,crud:CrudForgery,authentication:Optional[Authentication]=None,get_session:Optional[callable]=None):
        self.crud=crud
        self.PydanticModel=PydanticModel
        self.CreatePydanticModel=crud.CreatePydanticModel
        self.UpdatePydanticModel=crud.UpdatePydanticModel
        self.router = APIRouter(
            prefix=prefix,
            tags=tags,
            dependencies=(
                [
                    Depends(authentication.get_access_token)  ,
                    Depends(authentication.get_session),
                ]
                if authentication
                else [Depends(get_session) if get_session else Depends()]
            ),
        )
    def initialize_router(self,init_data:dict[str,bool]):

        if init_data.get('count')and init_data['count'] :
            @self.router.get(f"/count")
            async def count():
                count= await self.crud.count()
                return {'count':count}

        if init_data.get('read-one')and init_data['read-one'] :
            @self.router.get("/read-one/{id}",response_model=self.PydanticModel)
            async def read_one(id:int):
                return await self.crud.read_one(id)

        if init_data.get("read-all") and init_data["read-all"]:
            @self.router.get("/read-all",response_model=List[self.PydanticModel])
            async def read_all(skip:int=0,limit:int=None):
                return await self.crud.read_all(skip=skip,limit=limit)

        if init_data.get("read-all-by-filter") and init_data["read-all-by-filter"]:
            @self.router.get("/read-all-by-filter",response_model=List[self.PydanticModel])
            async def read_all_by_filter(filter:str,value:str,skip:int=0,limit:int=None):
                return await self.crud.read_all_by_filter(skip=skip,limit=limit,filter=filter, value=value)

        if init_data.get("create") and init_data["create"]:
            @self.router.post("/create", response_model=self.PydanticModel)
            async def create(create_obj:self.CreatePydanticModel):
                return await self.crud.create(create_obj)

        if init_data.get("update") and init_data["update"]:
            @self.router.put("/update/{id}", response_model=self.PydanticModel)
            async def update(id:int,update_obj:self.UpdatePydanticModel):
                return await self.crud.update(id, update_obj)

        if init_data.get("delete") and init_data["delete"]:
            @self.router.delete("/delete/{id}")
            async def delete(id:int):
                return await self.crud.delete(id)


class CustomProvideRouter:
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
        self.PydanticModel = PydanticModel
        self.CreatePydanticModel = crud.CreatePydanticModel
        self.UpdatePydanticModel = crud.UpdatePydanticModel
        self.token_dependency=Depends(get_access_token) if get_access_token else Depends(None),
        self.router = APIRouter(
            prefix=prefix,
            tags=tags,
            dependencies= [
                    Depends(get_session),
                ]
            ,
        )

    def initialize_router(self, init_data: List[RouteConfig]):
        for config in init_data:
            if config.router_name ==  "count" and config.is_activated:
                @self.router.get(
                        f"/count",
                        dependencies=[
                            (
                                self.token_dependency
                                if config.is_protected
                                else Depends(None)
                            )
                        ]
                    )
                async def count():
                    count = await self.crud.count()
                    return {"count": count}

            if config.router_name ==  "read-one" and config.is_activated:
                @self.router.get(
                    "/read-one/{id}",
                    response_model=self.PydanticModel,
                    dependencies=[
                        (
                            self.token_dependency
                            if config.is_protected
                            else Depends(None)
                        )
                    ],
                )
                async def read_one(id: int):
                    return await self.crud.read_one(id)

            if config.route_name=="read-all" and config.is_activated:
                @self.router.get(
                    "/read-all",
                    response_model=List[self.PydanticModel],
                    dependencies=[
                        (self.token_dependency if config.is_protected else Depends(None))
                    ],
                )
                async def read_all(skip: int = 0, limit: int = None):
                    return await self.crud.read_all(skip=skip, limit=limit)

        if config.route_name == "read-all-by-filter" and config.is_activated:

            @self.router.get(
                "/read-all-by-filter",
                response_model=List[self.PydanticModel],
                dependencies=[
                    (self.token_dependency if config.is_protected else Depends(None))
                ],
            )
            async def read_all_by_filter(
                filter: str, value: str, skip: int = 0, limit: int = None
            ):
                return await self.crud.read_all_by_filter(
                    skip=skip, limit=limit, filter=filter, value=value
                )

            if config.route_name == "create" and config.is_activated:

                @self.router.post(
                    "/create",
                    response_model=self.PydanticModel,
                    dependencies=[
                        (self.token_dependency if config.is_protected else Depends(None))
                    ],
                )
                async def create(create_obj: self.CreatePydanticModel):
                    return await self.crud.create(create_obj)

            if config.route_name=="update" and config.is_activated:

                @self.router.put(
                    "/update/{id}",
                    response_model=self.PydanticModel,
                    dependencies=[
                        (self.token_dependency if config.is_protected else Depends(None))
                    ],
                )
                async def update(id: int, update_obj: self.UpdatePydanticModel):
                    return await self.crud.update(id, update_obj)

            if  config.route_name=="delete" and config.is_activated:

                @self.router.delete(
                    "/delete/{id}",
                    dependencies=[
                        (self.token_dependency if config.is_protected else Depends(None))
                    ],
                )
                async def delete(id: int):
                    return await self.crud.delete(id)
