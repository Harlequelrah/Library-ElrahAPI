from myproject.settings.database import authentication
from elrahapi.authorization.privilege_model import RolePrivilegeCreateModel, RolePrivilegeUpdateModel
from elrahapi.crud.crud_forgery import CrudForgery
from myproject.settings.database import authentication
from elrahapi.authorization.privilege_model import (
    PrivilegeCreateModel,
    PrivilegeUpdateModel,
)
from elrahapi.authorization.role_model import (
    RoleCreateModel,
    RoleUpdateModel,
)
from .user_models import Privilege, Role, RolePrivilege , UserPrivilege
from elrahapi.authorization.privilege_model import PrivilegeCreateModel
from elrahapi.user.models import UserPrivilegeCreateModel,UserPrivilegeUpdateModel
from elrahapi.crud.user_crud_forgery import UserCrudForgery



userCrud = UserCrudForgery(authentication)

roleCrud = CrudForgery(
    entity_name="role",
    SQLAlchemyModel=Role,
    CreatePydanticModel=RoleCreateModel,
    UpdatePydanticModel=RoleUpdateModel,
    authentication=authentication
)

privilegeCrud = CrudForgery(
    entity_name="privilege",
    SQLAlchemyModel=Privilege,
    CreatePydanticModel=PrivilegeCreateModel,
    UpdatePydanticModel=PrivilegeUpdateModel,
    authentication=authentication,
)


userPrivilegeCrud=CrudForgery(
    entity_name='user_privilege',
    authentication=authentication,
    SQLAlchemyModel=UserPrivilege,
    CreatePydanticModel=UserPrivilegeCreateModel,
    UpdatePydanticModel= UserPrivilegeUpdateModel
)

rolePrivilegeCrud=CrudForgery(
    entity_name='role_privilege',
    authentication=authentication,
    SQLAlchemyModel=RolePrivilege,
    CreatePydanticModel=RolePrivilegeCreateModel,
    UpdatePydanticModel= RolePrivilegeUpdateModel

)
