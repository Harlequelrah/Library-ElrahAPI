

from harlequelrah_fastapi.router.user_router_provider import UserRouterProvider
from harlequelrah_fastapi.authorization.privilege_model import (
    PrivilegePydanticModel,
)
from harlequelrah_fastapi.authorization.role_model import (
    RolePydanticModel,
)
from harlequelrah_fastapi.authorization.role_privilege_model import RolePrivilegePydanticModel
from harlequelrah_fastapi.router.router_provider import CustomRouterProvider
from harlequelrah_fastapi.user.models import UserPrivilegePydanticModel

from .user_cruds import privilegeCrud, roleCrud , userPrivilegeCrud , userCrud



user_router_provider = UserRouterProvider(
    prefix="/users",
    tags=["users"],
    crud=userCrud,
)


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

user_privilege_router_provider=CustomRouterProvider(
    prefix='/users/privileges',
    tags=["users_privileges"],
    PydanticModel=UserPrivilegePydanticModel,
    crud=userPrivilegeCrud
)

role_privilege_router_provider=CustomRouterProvider(
    prefix='/roles/privileges',
    tags=["roles_privileges"],
    PydanticModel=RolePrivilegePydanticModel,
    crud=userPrivilegeCrud
)
