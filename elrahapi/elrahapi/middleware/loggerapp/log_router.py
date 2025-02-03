from elrahapi.router.router_namespace import DefaultRoutesName
from elrahapi.router.router_provider import CustomRouterProvider
from .log_crud import logCrud
from .log_schema import LoggerMiddlewarePydanticModel as LMPD

router_provider = CustomRouterProvider(
    prefix="/logs",
    tags=["logs"],
    PydanticModel=LMPD,
    crud=logCrud,
)
app_logger = router_provider.get_public_router(
    exclude_routes_name=[DefaultRoutesName.UPDATE, DefaultRoutesName.DELETE, DefaultRoutesName.CREATE]
)
