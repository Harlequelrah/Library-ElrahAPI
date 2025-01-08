from my_project.settings.database import authentication
from harlequelrah_fastapi.authorization.privilege.privilege_model import PrivilegeCreateModel,PrivilegeUpdateModel,PrivilegePydanticModel
from harlequelrah_fastapi.authorization.role.role_model import RoleCreateModel,RoleUpdateModel,RolePydanticModel
from harlequelrah_fastapi.router.router_provider import CustomRouterProvider

from .authorization_crud import privilegeCrud, roleCrud


role_router_provider = CustomRouterProvider(
    prefix="/roles",
    tags=["roles"],
    PydanticModel=RolePydanticModel,
    crud=roleCrud,
    get_access_token=authentication.get_access_token,
)

privilege_router_provider = CustomRouterProvider(
    prefix="/privileges",
    tags=["privileges"],
    PydanticModel=PrivilegePydanticModel,
    crud=privilegeCrud,
    get_access_token=authentication.get_access_token,
)


app_role = role_router_provider.get_protected_router()
app_privilege = privilege_router_provider.get_protected_router()
