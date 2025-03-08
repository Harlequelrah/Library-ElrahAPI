

from elrahapi.router.user_router_provider import UserRouterProvider
from elrahapi.authorization.privilege_model import (
    PrivilegePydanticModel,
)
from elrahapi.authorization.role_model import (
    RolePydanticModel,
)
from elrahapi.authorization.role_privilege_model import RolePrivilegePydanticModel
from elrahapi.router.router_provider import CustomRouterProvider
from elrahapi.authorization.user_privilege_model import UserPrivilegePydanticModel

from .user_cruds import privilegeCrud, roleCrud , userPrivilegeCrud , userCrud,rolePrivilegeCrud



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
    crud=rolePrivilegeCrud
)
