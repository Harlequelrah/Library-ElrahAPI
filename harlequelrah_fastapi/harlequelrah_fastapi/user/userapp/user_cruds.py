from myproject.settings.database import authentication
from harlequelrah_fastapi.authorization.role_privilege_model import RolePrivilegeCreateModel, RolePrivilegeUpdateModel
from harlequelrah_fastapi.crud.crud_forgery import CrudForgery
from myproject.settings.database import authentication
from harlequelrah_fastapi.authorization.privilege_model import (
    PrivilegeCreateModel,
    PrivilegeUpdateModel,
)
from harlequelrah_fastapi.authorization.role_model import (
    RoleCreateModel,
    RoleUpdateModel,
)
from harlequelrah_fastapi.crud.link_class import LinkClass
from .user_models import Privilege, Role, RolePrivilege , UserPrivilege
from harlequelrah_fastapi.user.models import UserPrivilegeCreateModel,UserPrivilegeUpdateModel
from harlequelrah_fastapi.crud.user_crud_forgery import UserCrudForgery



userCrud = UserCrudForgery(authentication)

roleCrud = CrudForgery(
    entity_name="role",
    SQLAlchemyModel=Role,
    CreatePydanticModel=RoleCreateModel,
    UpdatePydanticModel=RoleUpdateModel,
    authentication=authentication,
    Linked_Classes=[LinkClass(key='privileges',Model=Privilege)]
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
