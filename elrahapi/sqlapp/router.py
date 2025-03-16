from elrahapi.router.route_config import  RouteConfig
from elrahapi.router.router_default_routes_name import DefaultRoutesName
from myproject.myapp.cruds import myapp_crud
from myproject.myapp.schemas import EntityPydanticModel
# from myproject.settings.auth_configs import authentication
from typing import List
from elrahapi.router.router_provider import CustomRouterProvider

router_provider = CustomRouterProvider(
    prefix="/items",
    tags=["item"],
    crud=myapp_crud,
    # authentication= authentication
)

app_myapp = router_provider.get_public_router()

#Assurez vous d'avoir l'authentification dans le router_provider
# app_myapp = router_provider.get_protected_router()

# init_data: List[RouteConfig] = [
#     RouteConfig(route_name=DefaultRoutesName.CREATE, is_activated=True),
#     RouteConfig(route_name=DefaultRoutesName.READ_ONE, is_activated=True),
#     RouteConfig(route_name=DefaultRoutesName.READ_ALL, is_activated=True),
#     RouteConfig(route_name=DefaultRoutesName.UPDATE, is_activated=True, is_protected=True),
#     RouteConfig(route_name=DefaultRoutesName.DELETE, is_activated=True, is_protected=True),
# ]
# app_myapp = router_provider.initialize_router(init_data=init_data)
