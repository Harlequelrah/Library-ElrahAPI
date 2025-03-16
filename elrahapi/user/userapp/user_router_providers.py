

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

user_privilege_router_provider=CustomRouterProvider(
    prefix='/users/privileges',
    tags=["users_privileges"],
    PydanticModel=UserPrivilegePydanticModel,
    crud=userPrivilegeCrud
)

