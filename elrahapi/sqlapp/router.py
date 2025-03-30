from .cruds import myapp_crud
from ..settings.auth.configs import authentication
from elrahapi.router.router_default_routes_name import DefaultRoutesName
from typing import List
from elrahapi.router.router_provider import CustomRouterProvider

router_provider = CustomRouterProvider(
    prefix="/items",
    tags=["item"],
    crud=myapp_crud,
)

app_myapp = router_provider.get_public_router()
##app_myapp = router_provider.get_protected_router()

