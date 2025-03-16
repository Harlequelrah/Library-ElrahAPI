from elrahapi.crud.crud_forgery import CrudForgery
from myproject.settings.database import authentication
from elrahapi.authorization.privilege_model import PrivilegeCreateModel, PrivilegePatchModel, PrivilegeUpdateModel
from elrahapi.authorization.role_model import RoleCreateModel, RolePatchModel, RoleUpdateModel
from elrahapi.authorization.role_privilege_model import RolePrivilegeCreateModel, RolePrivilegePatchModel, RolePrivilegeUpdateModel
from elrahapi.crud.crud_models import CrudModels
from .authorization_models import Role,Privilege,RolePrivilege


role_crud_models=CrudModels(
    entity_name='role',
    primary_key_name='id',
    SQLAlchemyModel=Role,
    CreateModel= RoleCreateModel,
    UpdateModel=RoleUpdateModel,
    PatchModel=RolePatchModel
)

privilege_crud_models=CrudModels(
    entity_name='privilege',
    primary_key_name='id',
    SQLAlchemyModel=Privilege,
    CreateModel=PrivilegeCreateModel,
    UpdateModel=PrivilegeUpdateModel,
    PatchModel=PrivilegePatchModel
)

role_privilege_crud_models=CrudModels(
    entity_name='role_privilege',
    primary_key_name='id',
    SQLAlchemyModel=RolePrivilege,
    CreateModel=RolePrivilegeCreateModel,
    UpdateModel=RolePrivilegeUpdateModel,
    PatchModel=RolePrivilegePatchModel,
)


roleCrud = CrudForgery(
session_factory=authentication.session_factory,
crud_models=role_crud_models
)

privilegeCrud = CrudForgery(
session_factory=authentication.session_factory,
crud_models=privilege_crud_models
)

rolePrivilegeCrud=CrudForgery(
session_factory=authentication.session_factory,
crud_models=role_privilege_crud_models
)
