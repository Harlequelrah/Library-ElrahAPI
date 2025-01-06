from my_project.userapp.user_crud import userCrud
from sqlalchemy.orm import Session
from typing import List
from harlequelrah_fastapi.router.route_config import RouteConfig
from harlequelrah_fastapi.router.router_crud import get_single_route
from harlequelrah_fastapi.router.router_namespace import (
    DEFAULTROUTESNAME,
    USER_AUTH_CONFIG_ROUTES,
)
from harlequelrah_fastapi.router.user_router_provider import UserRouterProvider


user_router_provider = UserRouterProvider(
    prefix="/users",
    tags=["users"],
    crud=userCrud,
)
app_user = user_router_provider.get_mixed_router(
    init_data=USER_AUTH_CONFIG_ROUTES,
    public_routes_name=[DEFAULTROUTESNAME.CREATE],
    protected_routes_name=[DEFAULTROUTESNAME.READ_ALL_BY_FILTER],
)
