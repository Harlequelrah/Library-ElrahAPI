from .database import authentication
from myproject.userapp_user.models import User
# from myproject.userapp_admin.models import Admin
from elrahapi.crud.crud_forgery import CrudForgery
from .database import authentication,Base
from elrahapi.authorization.privilege_model import PrivilegeCreateModel, PrivilegePatchModel, PrivilegeUpdateModel
from elrahapi.authorization.role_model import RoleCreateModel, RolePatchModel, RoleUpdateModel
from elrahapi.authorization.role_privilege_model import RolePrivilegeCreateModel, RolePrivilegePatchModel, RolePrivilegeUpdateModel
from elrahapi.crud.crud_models import CrudModels
from sqlalchemy.orm import relationship
from elrahapi.authorization.role_model import RoleModel
from elrahapi.authorization.privilege_model import PrivilegeModel
from elrahapi.authorization.role_privilege_model import RolePrivilegeModel
from elrahapi.authorization.privilege_model import PrivilegeModel
from elrahapi.router.router_provider import CustomRouterProvider



authentication.authentication_models = {
    'User': User,
}
authentication_router = authentication.get_auth_router()

class Role(RoleModel,Base):
    __tablename__ = "roles"
    users = relationship("User", back_populates="role")
    # admins = relationship("Admin", back_populates="role")
    role_privileges = relationship(
        "RolePrivilege",  back_populates="role"
    )

class RolePrivilege(RolePrivilegeModel,Base):
    __tablename__= 'role_privileges'
    role= relationship("Role",back_populates='role_privileges')
    privilege=relationship("Privilege",back_populates="privilege_roles")

class Privilege(PrivilegeModel,Base):
    __tablename__ = "privileges"
    privilege_roles = relationship(
        "RolePrivilege",  back_populates="privilege"
    )
    privilege_users = relationship("UserPrivilege", back_populates="privilege")
    # privilege_admins = relationship("AdminPrivilege", back_populates="privilege")


metadata= Base.metadata


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

role_router_provider = CustomRouterProvider(
    prefix="/roles",
    tags=["roles"],
    crud=roleCrud,
)

privilege_router_provider = CustomRouterProvider(
    prefix="/privileges",
    tags=["privileges"],
    crud=privilegeCrud,
)



role_privilege_router_provider=CustomRouterProvider(
    prefix='/roles/privileges',
    tags=["roles_privileges"],
    crud=rolePrivilegeCrud)

role_router=role_router_provider.get_protected_router()

privilege_router=privilege_router_provider.get_protected_router()

role_privilege_router=role_privilege_router_provider.get_protected_router()
