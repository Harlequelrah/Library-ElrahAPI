from elrahapi.crud.crud_forgery import CrudForgery

from elrahapi.authorization.role.schemas import (
    RoleCreateModel,
    RoleFullReadModel,
    RolePatchModel,
    RoleReadModel,
    RoleUpdateModel,
)

from elrahapi.authorization.privilege.schemas import (
    PrivilegeCreateModel,
    PrivilegeFullReadModel,
    PrivilegePatchModel,
    PrivilegeReadModel,
    PrivilegeUpdateModel,
)

from elrahapi.authorization.role_privilege.schemas import (
    RolePrivilegeCreateModel,
    RolePrivilegeFullReadModel,
    RolePrivilegePatchModel,
    RolePrivilegeReadModel,
    RolePrivilegeUpdateModel,
)

from elrahapi.authorization.user_privilege.schemas import (
    UserPrivilegeCreateModel,
    UserPrivilegeFullReadModel,
    UserPrivilegePatchModel,
    UserPrivilegeReadModel,
    UserPrivilegeUpdateModel,
)

from elrahapi.authorization.user_role.schemas import (
    UserRoleCreateModel,
    UserRoleFullReadModel,
    UserRolePatchModel,
    UserRoleReadModel,
    UserRoleUpdateModel,
)

from elrahapi.crud.crud_models import CrudModels
from .models import User, UserPrivilege, Role, Privilege, RolePrivilege, UserRole
from .schemas import (
    UserCreateModel,
    UserUpdateModel,
    UserPatchModel,
    UserReadModel,
    UserFullReadModel,
)
from ..database import database
from elrahapi.crud.crud_forgery import CrudForgery

user_crud_models = CrudModels(
    entity_name="user",
    primary_key_name="id",
    SQLAlchemyModel=User,
    CreateModel=UserCreateModel,
    UpdateModel=UserUpdateModel,
    PatchModel=UserPatchModel,
    ReadModel=UserReadModel,
    FullReadModel=UserFullReadModel,
)

role_crud_models = CrudModels(
    entity_name="role",
    primary_key_name="id",
    SQLAlchemyModel=Role,
    CreateModel=RoleCreateModel,
    UpdateModel=RoleUpdateModel,
    PatchModel=RolePatchModel,
    ReadModel=RoleReadModel,
    FullReadModel=RoleFullReadModel,
)

privilege_crud_models = CrudModels(
    entity_name="privilege",
    primary_key_name="id",
    SQLAlchemyModel=Privilege,
    CreateModel=PrivilegeCreateModel,
    UpdateModel=PrivilegeUpdateModel,
    PatchModel=PrivilegePatchModel,
    ReadModel=PrivilegeReadModel,
    FullReadModel=PrivilegeFullReadModel,
)

role_privilege_crud_models = CrudModels(
    entity_name="role_privilege",
    primary_key_name="id",
    SQLAlchemyModel=RolePrivilege,
    CreateModel=RolePrivilegeCreateModel,
    UpdateModel=RolePrivilegeUpdateModel,
    PatchModel=RolePrivilegePatchModel,
    ReadModel=RolePrivilegeReadModel,
    FullReadModel=RolePrivilegeFullReadModel,
)


user_privilege_crud_models = CrudModels(
    entity_name="user_privilege",
    primary_key_name="id",
    SQLAlchemyModel=UserPrivilege,
    CreateModel=UserPrivilegeCreateModel,
    UpdateModel=UserPrivilegeUpdateModel,
    PatchModel=UserPrivilegePatchModel,
    ReadModel=UserPrivilegeReadModel,
    FullReadModel=UserPrivilegeFullReadModel,
)

user_role_crud_models = CrudModels(
    entity_name="user_role",
    primary_key_name="id",
    SQLAlchemyModel=UserRole,
    CreateModel=UserRoleCreateModel,
    UpdateModel=UserRoleUpdateModel,
    PatchModel=UserRolePatchModel,
    ReadModel=UserRoleReadModel,
    FullReadModel=UserRoleFullReadModel,
)

user_privilege_crud = CrudForgery(
    crud_models=user_privilege_crud_models, session_manager=database.session_manager
)


user_crud = CrudForgery(
    crud_models=user_crud_models, session_manager=database.session_manager
)

role_crud = CrudForgery(
    crud_models=role_crud_models, session_manager=database.session_manager
)

privilege_crud = CrudForgery(
    crud_models=privilege_crud_models, session_manager=database.session_manager
)

role_privilege_crud = CrudForgery(
    crud_models=role_privilege_crud_models, session_manager=database.session_manager
)


user_role_crud = CrudForgery(
    crud_models=user_role_crud_models, session_manager=database.session_manager
)
