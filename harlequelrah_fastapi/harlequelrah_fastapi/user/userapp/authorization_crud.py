from harlequelrah_fastapi.crud.crud_forgery import CrudForgery
from my_project.settings.database import authentication
from harlequelrah_fastapi.authorization.privilege_model import (
    PrivilegeCreateModel,
    PrivilegeUpdateModel,
)
from harlequelrah_fastapi.authorization.role_model import (
    RoleCreateModel,
    RoleUpdateModel,
)
from .user_model import Privilege, Role


roleCrud = CrudForgery(
    entity_name="role",
    SQLAlchemyModel=Role,
    CreatePydanticModel=RoleCreateModel,
    UpdatePydanticModel=RoleUpdateModel,
    authentication=authentication,
)

privilegeCrud = CrudForgery(
    entity_name="privilege",
    SQLAlchemyModel=Privilege,
    CreatePydanticModel=PrivilegeCreateModel,
    UpdatePydanticModel=PrivilegeUpdateModel,
    authentication=authentication,
)
