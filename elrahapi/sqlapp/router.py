from elrahapi.router.router_namespace import DefaultRoutesName, TypeRoute
from elrahapi.router.router_provider import CustomRouterProvider
from myproject.myapp.cruds import myapp_crud
from myproject.settings.config.auth_config import authentication

router_provider = CustomRouterProvider(
    prefix="/items",
    tags=["item"],
    crud=myapp_crud,
    # authentication=authentication,
)

myapp_router = router_provider.get_public_router()
# myapp_router = router_provider.get_protected_router()
