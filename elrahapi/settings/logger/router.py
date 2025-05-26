from elrahapi.router.router_namespace import DefaultRoutesName, TypeRoute
from elrahapi.router.router_provider import CustomRouterProvider
from .crud import logCrud
from ..auth.configs import authentication
from ..database import session_manager
router_provider = CustomRouterProvider(
    prefix="/logs",
    tags=["logs"],
    crud=logCrud,
    authentication=authentication,
    session_manager=session_manager
)
logger_router = router_provider.get_custom_router(
    routes_name=[DefaultRoutesName.READ_ONE, DefaultRoutesName.READ_ALL],
    type_route=TypeRoute.PROTECTED
)

