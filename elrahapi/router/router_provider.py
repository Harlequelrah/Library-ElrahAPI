from typing import List, Optional

from elrahapi.authentication.authentication_manager import AuthenticationManager
from elrahapi.crud.bulk_models import BulkDeleteModel
from elrahapi.crud.crud_forgery import CrudForgery
from elrahapi.exception.auth_exception import NO_AUTHENTICATION_PROVIDED_CUSTOM_HTTP_EXCEPTION
from elrahapi.router.route_config import AuthorizationConfig, RouteConfig
from fastapi import status
from elrahapi.router.router_crud import (
    format_init_data,
    get_single_route,
    initialize_dependecies,
)
from elrahapi.router.router_namespace import (
    ROUTES_PROTECTED_CONFIG,
    ROUTES_PUBLIC_CONFIG,
    DefaultRoutesName,
    TypeRoute,
)

from fastapi import APIRouter


class CustomRouterProvider:

    def __init__(
        self,
        prefix: str,
        tags: List[str],
        crud: CrudForgery,
        roles: Optional[List[str]] = None,
        privileges: Optional[List[str]] = None,
        authentication:Optional[AuthenticationManager]=None,
    ):
        self.authentication:AuthenticationManager = authentication if authentication else None
        self.get_access_token:Optional[callable]= authentication.get_access_token if authentication else None
        self.session_factory: callable = crud.session_factory
        self.pk = crud.crud_models.primary_key_name
        self.PydanticModel = crud.PydanticModel
        self.CreatePydanticModel = crud.CreatePydanticModel
        self.UpdatePydanticModel = crud.UpdatePydanticModel
        self.PatchPydanticModel = crud.PatchPydanticModel
        self.crud=crud
        self.roles = roles
        self.privileges = privileges
        self.router = APIRouter(
            prefix=prefix,
            tags=tags,
        )

    def get_public_router(
        self, exclude_routes_name: Optional[List[DefaultRoutesName]] = None
    ) -> APIRouter:
        return self.initialize_router(ROUTES_PUBLIC_CONFIG, exclude_routes_name)

    def get_protected_router(
        self,
        authorizations: Optional[List[AuthorizationConfig]] = None,
        exclude_routes_name: Optional[List[DefaultRoutesName]] = None,
    ) -> APIRouter:
        if not self.authentication : raise NO_AUTHENTICATION_PROVIDED_CUSTOM_HTTP_EXCEPTION
        return self.initialize_router(
            init_data=ROUTES_PROTECTED_CONFIG,
            exclude_routes_name=exclude_routes_name,
            authorizations=authorizations,
        )


    def get_custom_router_init_data(self, init_data: Optional[List[RouteConfig]] = None,route_names: Optional[List[DefaultRoutesName]] = None,is_protected:TypeRoute=TypeRoute.PUBLIC):
        custom_init_data = init_data if init_data else []
        if route_names:
            for route_name in route_names:
                if is_protected==TypeRoute.PROTECTED  and not self.authentication :
                    raise NO_AUTHENTICATION_PROVIDED_CUSTOM_HTTP_EXCEPTION
                route = get_single_route(route_name,is_protected)
                custom_init_data.append(route)
        return custom_init_data

    def get_custom_public_router(
        self,
        init_data: Optional[List[RouteConfig]] = None,
        public_routes_name: Optional[List[DefaultRoutesName]] = None,
        exclude_routes_name: Optional[List[DefaultRoutesName]] = None,
    ):
        custom_init_data=self.get_custom_router_init_data(init_data,public_routes_name)
        return self.initialize_router(custom_init_data,exclude_routes_name=exclude_routes_name)


    def get_custom_protected_router(
        self,
        init_data: Optional[List[RouteConfig]] = None,
        protected_routes_name: Optional[List[DefaultRoutesName]] = None,
        authorizations: Optional[List[AuthorizationConfig]] =None,
        exclude_routes_name: Optional[List[DefaultRoutesName]] = None,
    ):
        if not self.authentication : raise NO_AUTHENTICATION_PROVIDED_CUSTOM_HTTP_EXCEPTION
        custom_init_data=self.get_custom_router_init_data(init_data,protected_routes_name,is_protected=True)
        return self.initialize_router(custom_init_data,exclude_routes_name=exclude_routes_name,authorizations=authorizations)

    def get_mixed_router(
        self,
        init_data: Optional[List[RouteConfig]] = None,
        public_routes_name: Optional[List[DefaultRoutesName]] = None,
        protected_routes_name: Optional[List[DefaultRoutesName]] = None,
        exclude_routes_name: Optional[List[DefaultRoutesName]] = None,
    ) -> APIRouter:
        if not self.authentication : raise NO_AUTHENTICATION_PROVIDED_CUSTOM_HTTP_EXCEPTION
        if init_data is None:
            init_data = []
        public_routes_data = self.get_custom_router_init_data(init_data, public_routes_name)
        protected_routes_data=self.get_custom_router_init_data(init_data, protected_routes_name,is_protected=True)
        custom_init_data=public_routes_data+protected_routes_data
        return self.initialize_router(custom_init_data,exclude_routes_name)



    def initialize_router(
        self,
        init_data: List[RouteConfig],
        authorizations: Optional[List[AuthorizationConfig]] = None,
        exclude_routes_name: Optional[List[DefaultRoutesName]] = None,
    ) -> APIRouter:
        init_data = format_init_data(
            init_data=init_data,
            authorizations=authorizations,
            exclude_routes_name=exclude_routes_name,
        )
        for config in init_data:
            if config.route_name == DefaultRoutesName.COUNT and config.is_activated:
                dependencies = initialize_dependecies(
                    config=config,
                    authentication=self.authentication,
                    roles=self.roles,
                    privileges=self.privileges,
                )

                @self.router.get(
                    path=config.route_path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    dependencies=dependencies,
                )
                async def count():
                    count = await self.crud.count()
                    return {"count": count}

            if config.route_name == DefaultRoutesName.READ_ONE and config.is_activated:
                dependencies = initialize_dependecies(
                    config=config,
                    authentication=self.authentication,
                    roles=self.roles,
                    privileges=self.privileges,
                )
                path = f"{config.route_path}/{{pk}}" if "{pk}" not in config.route_path else config.route_path

                @self.router.get(
                    path=path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    response_model=self.PydanticModel,
                    dependencies=dependencies,
                )
                async def read_one(
                    pk,
                ):
                    return await self.crud.read_one(pk)

            if config.route_name == DefaultRoutesName.READ_ALL and config.is_activated:
                dependencies = initialize_dependecies(
                    config=config,
                    authentication=self.authentication,
                    roles=self.roles,
                    privileges=self.privileges,
                )

                @self.router.get(
                    path=config.route_path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    response_model=List[self.PydanticModel],
                    dependencies=dependencies,
                )
                async def read_all(
                    filter: Optional[str] = None,
                    value=None,
                    skip: int = 0,
                    limit: int = None,
                ):
                    return await self.crud.read_all(
                        skip=skip, limit=limit, filter=filter, value=value
                    )

            if (
                config.route_name == DefaultRoutesName.CREATE
                and self.CreatePydanticModel
                and config.is_activated
            ):
                dependencies = initialize_dependecies(
                    config=config,
                    authentication=self.authentication,
                    roles=self.roles,
                    privileges=self.privileges,
                )

                @self.router.post(
                    path=config.route_path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    response_model=self.PydanticModel,
                    dependencies=dependencies,
                    status_code = status.HTTP_201_CREATED
                )
                async def create(
                    create_obj: self.CreatePydanticModel,
                ):
                    return await self.crud.create(create_obj)

            if (
                config.route_name == DefaultRoutesName.UPDATE
                and self.UpdatePydanticModel
                and config.is_activated
            ):
                dependencies = initialize_dependecies(
                    config=config,
                    authentication=self.authentication,
                    roles=self.roles,
                    privileges=self.privileges,
                )
                path = f"{config.route_path}/{{pk}}" if "{pk}" not in config.route_path else config.route_path

                @self.router.put(
                    path=path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    response_model=self.PydanticModel,
                    dependencies=dependencies,
                )
                async def update(
                    pk,
                    update_obj: self.UpdatePydanticModel,
                ):
                    return await self.crud.update(pk, update_obj, True)

            if (
                config.route_name == DefaultRoutesName.PATCH
                and self.PatchPydanticModel
                and config.is_activated
            ):
                dependencies = initialize_dependecies(
                    config=config,
                    authentication=self.authentication,
                    roles=self.roles,
                    privileges=self.privileges,
                )
                path = f"{config.route_path}/{{pk}}" if "{pk}" not in config.route_path else config.route_path

                @self.router.patch(
                    path=path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    response_model=self.PydanticModel,
                    dependencies=dependencies,
                )
                async def patch(
                    pk,
                    update_obj: self.PatchPydanticModel,
                ):
                    return await self.crud.update(pk, update_obj, False)

            if config.route_name == DefaultRoutesName.DELETE and config.is_activated:
                dependencies = initialize_dependecies(
                    config=config,
                    authentication=self.authentication,
                    roles=self.roles,
                    privileges=self.privileges,
                )
                path = f"{config.route_path}/{{pk}}" if "{pk}" not in config.route_path else config.route_path

                @self.router.delete(
                    path=path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    dependencies=dependencies,
                    status_code=status.HTTP_204_NO_CONTENT,
                )
                async def delete(
                    pk,
                ):
                    return await self.crud.delete(pk)

            if (
                config.route_name == DefaultRoutesName.BULK_DELETE
                and config.is_activated
            ):
                dependencies = initialize_dependecies(
                    config=config,
                    authentication=self.authentication,
                    roles=self.roles,
                    privileges=self.privileges,
                )

                @self.router.delete(
                    path=config.route_path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    dependencies=dependencies,
                    status_code=status.HTTP_204_NO_CONTENT,
                )
                async def bulk_delete(
                    pk_list: BulkDeleteModel,
                ):
                    return await self.crud.bulk_delete(pk_list)

            if (
                config.route_name == DefaultRoutesName.BULK_CREATE
                and config.is_activated
            ):
                dependencies = initialize_dependecies(
                    config=config,
                    authentication=self.authentication,
                    roles=self.roles,
                    privileges=self.privileges,
                )

                @self.router.post(
                    path=config.route_path,
                    summary=config.summary if config.summary else None,
                    description=config.description if config.description else None,
                    dependencies=dependencies,
                )
                async def bulk_create(
                    create_obj_list: List[self.CreatePydanticModel],
                ):
                    return await self.crud.bulk_create(create_obj_list)

        return self.router
