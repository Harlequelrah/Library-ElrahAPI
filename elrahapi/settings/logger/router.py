from app.settings.config.auth_config import authentication
from app.settings.logger.crud import LogModel, logCrud
from elrahapi.middleware.middleware_helper import MiddlewareHelper
from elrahapi.router.router_namespace import DefaultRoutesName, TypeRoute
from elrahapi.router.router_provider import CustomRouterProvider

router_provider = CustomRouterProvider(
    prefix="/logs", tags=["logs"], crud=logCrud, authentication=authentication
)
logger_router = router_provider.get_custom_router(
    routes_name=[DefaultRoutesName.READ_ONE, DefaultRoutesName.READ_ALL],
    type_route=TypeRoute.PROTECTED,
)

# middleware_helper = MiddlewareHelper(LogModel=LogModel, authentication=authentication)
