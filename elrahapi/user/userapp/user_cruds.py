from myproject.settings.database import authentication
from elrahapi.authorization.role_privilege_model import RolePrivilegeCreateModel, RolePrivilegeUpdateModel,RolePrivilegePatchModel
from elrahapi.authorization.user_privilege_model import UserPrivilegePatchModel
from elrahapi.crud.crud_forgery import CrudForgery
from myproject.settings.database import authentication
from elrahapi.authorization.privilege_model import (
    PrivilegeCreateModel,
    PrivilegeUpdateModel,
    PrivilegePatchModel
)
from elrahapi.authorization.role_model import (
    RoleCreateModel,
    RoleUpdateModel,
    RolePatchModel
)
from .user_models import Privilege, Role, RolePrivilege , UserPrivilege
from elrahapi.authorization.privilege_model import PrivilegeCreateModel
from elrahapi.authorization.user_privilege_model import UserPrivilegeCreateModel,UserPrivilegeUpdateModel
from elrahapi.crud.user_crud_forgery import UserCrudForgery



userCrud = UserCrudForgery(authentication)

roleCrud = CrudForgery(
    entity_name="role",
    SQLAlchemyModel=Role,
    primary_key_name="id",
    CreatePydanticModel=RoleCreateModel,
    UpdatePydanticModel=RoleUpdateModel,
    PatchPydanticModel=RolePatchModel,
    authentication=authentication
)

privilegeCrud = CrudForgery(
    entity_name="privilege",
    SQLAlchemyModel=Privilege,
    primary_key_name="id",
    CreatePydanticModel=PrivilegeCreateModel,
    UpdatePydanticModel=PrivilegeUpdateModel,
    PatchPydanticModel=PrivilegePatchModel,
    authentication=authentication,
)


userPrivilegeCrud=CrudForgery(
    entity_name='user_privilege',
    primary_key_name="id",
    authentication=authentication,
    SQLAlchemyModel=UserPrivilege,
    CreatePydanticModel=UserPrivilegeCreateModel,
    UpdatePydanticModel= UserPrivilegeUpdateModel,
    PatchPydanticModel=UserPrivilegePatchModel,
)

rolePrivilegeCrud=CrudForgery(
    entity_name='role_privilege',
    authentication=authentication,
    primary_key_name="id",
    SQLAlchemyModel=RolePrivilege,
    CreatePydanticModel=RolePrivilegeCreateModel,
    UpdatePydanticModel= RolePrivilegeUpdateModel,
    PatchPydanticModel=RolePrivilegePatchModel,

)
