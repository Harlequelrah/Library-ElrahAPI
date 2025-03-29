
from elrahapi.authorization.privilege_model import PrivilegeCreateModel, PrivilegePatchModel, PrivilegePydanticModel, PrivilegeUpdateModel
from elrahapi.authorization.role_model import RoleCreateModel, RolePydanticModel,RoleUpdateModel,RolePatchModel
from elrahapi.authorization.role_privilege_model import RolePrivilegeCreateModel, RolePrivilegePatchModel, RolePrivilegePydanticModel, RolePrivilegeUpdateModel
from elrahapi.authorization.user_privilege_model import UserPrivilegePatchModel, UserPrivilegePydanticModel
from elrahapi.crud.crud_forgery import CrudForgery
from ..database import authentication
from elrahapi.crud.crud_models import CrudModels
from .models import User, UserPrivilege,Role,Privilege,RolePrivilege
from .schemas import UserCreateModel,UserUpdateModel,UserPatchModel,UserPydanticModel
from elrahapi.authorization.user_privilege_model import UserPrivilegeCreateModel,UserPrivilegeUpdateModel
from elrahapi.crud.crud_forgery import CrudForgery

user_crud_models = CrudModels(
    entity_name="user",
    primary_key_name="id",
    SQLAlchemyModel=User,
    CreateModel=UserCreateModel,
    UpdateModel=UserUpdateModel,
    PatchModel=UserPatchModel,
    PydanticModel=UserPydanticModel
)

role_crud_models=CrudModels(
    entity_name='role',
    primary_key_name='id',
    SQLAlchemyModel=Role,
    CreateModel= RoleCreateModel,
    UpdateModel=RoleUpdateModel,
    PatchModel=RolePatchModel,
    PydanticModel=RolePydanticModel
)

privilege_crud_models=CrudModels(
    entity_name='privilege',
    primary_key_name='id',
    SQLAlchemyModel=Privilege,
    CreateModel=PrivilegeCreateModel,
    UpdateModel=PrivilegeUpdateModel,
    PatchModel=PrivilegePatchModel,
    PydanticModel=PrivilegePydanticModel
)

role_privilege_crud_models=CrudModels(
    entity_name='role_privilege',
    primary_key_name='id',
    SQLAlchemyModel=RolePrivilege,
    CreateModel=RolePrivilegeCreateModel,
    UpdateModel=RolePrivilegeUpdateModel,
    PatchModel=RolePrivilegePatchModel,
    PydanticModel=RolePrivilegePydanticModel,
)



user_privilege_crud_models = CrudModels(
    entity_name="user_privilege",
    primary_key_name="id",
    SQLAlchemyModel=UserPrivilege,
    CreateModel=UserPrivilegeCreateModel,
    UpdateModel=UserPrivilegeUpdateModel,
    PatchModel=UserPrivilegePatchModel,
    PydanticModel=UserPrivilegePydanticModel
)

user_privilege_crud=CrudForgery(
    crud_models=user_privilege_crud_models,
    session_factory=authentication.session_factory
)


user_crud = CrudForgery(
    crud_models=user_crud_models,
    session_factory= authentication.session_factory
)

role_crud = CrudForgery(
session_factory=authentication.session_factory,
crud_models=role_crud_models
)

privilege_crud = CrudForgery(
session_factory=authentication.session_factory,
crud_models=privilege_crud_models
)

role_privilege_crud=CrudForgery(
session_factory=authentication.session_factory,
crud_models=role_privilege_crud_models
)


