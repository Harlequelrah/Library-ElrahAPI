from elrahapi.router.route_config import  RouteConfig
from myproject.settings.database import authentication
from myproject.myapp.cruds import myapp_crud
from myproject.myapp.models.schema import PydanticModel
from typing import List
from elrahapi.router.router_provider import CustomRouterProvider

router_provider = CustomRouterProvider(
    prefix="/items",
    tags=["item"],
    PydanticModel=PydanticModel,
    crud=myapp_crud
)

# app_myapp = router_provider.get_public_router()
# app_myapp = router_provider.get_protected_router()

init_data: List[RouteConfig] = [
    RouteConfig(route_name="create", is_activated=True),
    RouteConfig(route_name="read-one", is_activated=True),
    RouteConfig(route_name="update", is_activated=True, is_protected=True),
    RouteConfig(route_name="delete", is_activated=True, is_protected=True),
]
app_myapp = router_provider.initialize_router(init_data=init_data)
