from elrahapi.router.router_namespace import DefaultRoutesName
from elrahapi.router.router_provider import CustomRouterProvider
from .log_crud import logCrud
from .log_schema import LogPydanticModel

router_provider = CustomRouterProvider(
    prefix="/logs",
    tags=["logs"],
    PydanticModel=LogPydanticModel,
    crud=logCrud,
)
app_logger = router_provider.get_custom_public_router(
    public_routes_name=[DefaultRoutesName.READ_ONE, DefaultRoutesName.READ_ALL]
)
