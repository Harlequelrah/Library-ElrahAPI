
from elrahapi.authorization.privilege_model import PrivilegeCreateModel, PrivilegePatchModel, PrivilegeReadModel, PrivilegeUpdateModel,PrivilegeFullReadModel
from elrahapi.authorization.role_model import RoleCreateModel, RoleReadModel,RoleUpdateModel,RolePatchModel,RoleFullReadModel
from elrahapi.authorization.role_privilege_model import RolePrivilegeCreateModel, RolePrivilegePatchModel, RolePrivilegeReadModel, RolePrivilegeUpdateModel,RolePrivilegeFullReadModel
from elrahapi.authorization.user_privilege_model import UserPrivilegePatchModel, UserPrivilegeReadModel,UserPrivilegeFullReadModel
from elrahapi.authorization.user_role_model import UserRoleCreateModel, UserRolePatchModel, UserRoleReadModel, UserRoleUpdateModel,UserRoleFullReadModel
from elrahapi.crud.crud_forgery import CrudForgery
from ..database import session_manager
from elrahapi.crud.crud_models import CrudModels
from .models import User, UserPrivilege,Role,Privilege,RolePrivilege,UserRole
from .schemas import UserCreateModel,UserUpdateModel,UserPatchModel,UserReadModel,UserFullReadModel
from elrahapi.authorization.user_privilege_model import UserPrivilegeCreateModel,UserPrivilegeUpdateModel
from elrahapi.crud.crud_forgery import CrudForgery

user_crud_models = CrudModels(
    entity_name="user",
    primary_key_name="id",
    SQLAlchemyModel=User,
    CreateModel=UserCreateModel,
    UpdateModel=UserUpdateModel,
    PatchModel=UserPatchModel,
    ReadModel=UserReadModel,
    FullReadModel=UserFullReadModel
)

role_crud_models=CrudModels(
    entity_name='role',
    primary_key_name='id',
    SQLAlchemyModel=Role,
    CreateModel= RoleCreateModel,
    UpdateModel=RoleUpdateModel,
    PatchModel=RolePatchModel,
    ReadModel=RoleReadModel,
    FullReadModel=RoleFullReadModel
)

privilege_crud_models=CrudModels(
    entity_name='privilege',
    primary_key_name='id',
    SQLAlchemyModel=Privilege,
    CreateModel=PrivilegeCreateModel,
    UpdateModel=PrivilegeUpdateModel,
    PatchModel=PrivilegePatchModel,
    ReadModel=PrivilegeReadModel,
    FullReadModel=PrivilegeFullReadModel
)

role_privilege_crud_models=CrudModels(
    entity_name='role_privilege',
    primary_key_name='id',
    SQLAlchemyModel=RolePrivilege,
    CreateModel=RolePrivilegeCreateModel,
    UpdateModel=RolePrivilegeUpdateModel,
    PatchModel=RolePrivilegePatchModel,
    ReadModel=RolePrivilegeReadModel,
    FullReadModel=RolePrivilegeFullReadModel
)



user_privilege_crud_models = CrudModels(
    entity_name="user_privilege",
    primary_key_name="id",
    SQLAlchemyModel=UserPrivilege,
    CreateModel=UserPrivilegeCreateModel,
    UpdateModel=UserPrivilegeUpdateModel,
    PatchModel=UserPrivilegePatchModel,
    ReadModel=UserPrivilegeReadModel,
    FullReadModel=UserPrivilegeFullReadModel
)

user_role_crud_models = CrudModels(
    entity_name="user_role",
    primary_key_name="id",
    SQLAlchemyModel=UserRole,
    CreateModel=UserRoleCreateModel,
    UpdateModel=UserRoleUpdateModel,
    PatchModel=UserRolePatchModel,
    ReadModel=UserRoleReadModel,
    FullReadModel=UserRoleFullReadModel
)

user_privilege_crud=CrudForgery(
    crud_models=user_privilege_crud_models,
    session_manager=session_manager
)


user_crud = CrudForgery(
    crud_models=user_crud_models,
    session_manager=session_manager
)

role_crud = CrudForgery(
session_manager=session_manager,
crud_models=role_crud_models
)

privilege_crud = CrudForgery(
session_manager=session_manager,
crud_models=privilege_crud_models
)

role_privilege_crud=CrudForgery(
session_manager=session_manager,
crud_models=role_privilege_crud_models
)


user_role_crud=CrudForgery(
session_manager=session_manager,
crud_models=user_role_crud_models
)


