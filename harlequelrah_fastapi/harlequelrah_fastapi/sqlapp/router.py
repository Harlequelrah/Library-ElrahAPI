from harlequelrah_fastapi.router.route_config import RouteConfig
from myproject.settings.database import authentication
from myproject.myapp.cruds import myapp_crud
import myproject.myapp.models as model
from typing import List
from harlequelrah_fastapi.router.router_provider import CustomRouterProvider

router_provider = CustomRouterProvider(
    prefix="/items",
    tags=["item"],
    PydanticModel=model.PydanticModel,
    crud=myapp_crud,
    authentication=authentication
)

# app_todolist = router_provider.get_default_router()
# app_todolist = router_provider.get_protected_router()

init_data: List[RouteConfig] = [
    RouteConfig(route_name="create", is_activated=True),
    RouteConfig(route_name="read-one", is_activated=True),
    RouteConfig(route_name="update", is_activated=True, is_protected=True),
    RouteConfig(route_name="delete", is_activated=True, is_protected=True),
]
app_myapp = router_provider.initialize_router(init_data=init_data)
