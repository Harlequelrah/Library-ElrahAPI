from elrahapi.router.router_namespace import DefaultRoutesName
from elrahapi.router.router_provider import CustomRouterProvider
from .log_crud import logCrud
from myproject.settings.auth_configs import authentication
router_provider = CustomRouterProvider(
    prefix="/logs",
    tags=["logs"],
    crud=logCrud,
    authentication=authentication,
)
app_logger = router_provider.get_custom_public_router(
    public_routes_name=[DefaultRoutesName.READ_ONE, DefaultRoutesName.READ_ALL]
)
