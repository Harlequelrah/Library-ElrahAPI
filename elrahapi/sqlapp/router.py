from .cruds import myapp_crud
from ..settings.auth.configs import authentication
from elrahapi.router.router_namespace import DefaultRoutesName, TypeRoute
from typing import List
from elrahapi.router.router_provider import CustomRouterProvider

router_provider = CustomRouterProvider(
    prefix="/items",
    tags=["item"],
    crud=myapp_crud,
    #authentication=authentication,
)

app_myapp = router_provider.get_public_router()
##app_myapp = router_provider.get_protected_router()

