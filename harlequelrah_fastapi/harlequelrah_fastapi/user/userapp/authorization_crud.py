from harlequelrah_fastapi.crud.crud_forgery import CrudForgery
from my_project.settings.database import authentication
from harlequelrah_fastapi.authorization.privilege_model import (
    PrivilegeCreateModel,
    PrivilegeUpdateModel,
    PrivilegePydanticModel,
)
from harlequelrah_fastapi.authorization.role_model import (
    RoleCreateModel,
    RoleUpdateModel,
    RolePydanticModel,
)
from .user_model import Privilege, Role


roleCrud = CrudForgery(
    entity_name="role",
    session_factory=authentication.session_factory,
    SQLAlchemyModel=Role,
    CreatePydanticModel=RoleCreateModel,
    UpdatePydanticModel=RoleUpdateModel,
)

privilegeCrud = CrudForgery(
    entity_name="privilege",
    session_factory=authentication.session_factory,
    SQLAlchemyModel=Privilege,
    CreatePydanticModel=PrivilegeCreateModel,
    UpdatePydanticModel=PrivilegeUpdateModel,
)
