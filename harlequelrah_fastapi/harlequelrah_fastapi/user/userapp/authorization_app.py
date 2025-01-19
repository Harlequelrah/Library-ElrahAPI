from my_project.settings.database import authentication
from harlequelrah_fastapi.authorization.privilege_model import (
    PrivilegePydanticModel,
)
from harlequelrah_fastapi.authorization.role_model import (
    RolePydanticModel,
)
from harlequelrah_fastapi.router.router_provider import CustomRouterProvider

from .authorization_crud import privilegeCrud, roleCrud


role_router_provider = CustomRouterProvider(
    prefix="/roles",
    tags=["roles"],
    PydanticModel=RolePydanticModel,
    crud=roleCrud,
)

privilege_router_provider = CustomRouterProvider(
    prefix="/privileges",
    tags=["privileges"],
    PydanticModel=PrivilegePydanticModel,
    crud=privilegeCrud,
)


app_role = role_router_provider.get_protected_router()
app_privilege = privilege_router_provider.get_protected_router()
