from elrahapi.router.router_namespace import DefaultRoutesName, TypeRoute
from elrahapi.router.router_provider import CustomRouterProvider
from logger.crud import logCrud
from settings.auth.configs import authentication
router_provider = CustomRouterProvider(
    prefix="/logs",
    tags=["logs"],
    crud=logCrud,
    authentication=authentication
)
logger_router = router_provider.get_custom_router(
    routes_name=[DefaultRoutesName.READ_ONE, DefaultRoutesName.READ_ALL],
    type_route=TypeRoute.PROTECTED
)

