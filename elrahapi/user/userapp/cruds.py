
from elrahapi.authorization.user_privilege_model import UserPrivilegePatchModel
from elrahapi.crud.crud_forgery import CrudForgery
from myproject.settings.database import authentication
from elrahapi.crud.crud_models import CrudModels
from .models import User, UserPrivilege
from .schemas import UserCreateModel,UserUpdateModel,UserPatchModel
from elrahapi.authorization.user_privilege_model import UserPrivilegeCreateModel,UserPrivilegeUpdateModel
from elrahapi.crud.crud_forgery import CrudForgery

user_crud_models = CrudModels(
    entity_name="user",
    primary_key_name="id",
    SQLAlchemyModel=User,
    CreateModel=UserCreateModel,
    UpdateModel=UserUpdateModel,
    PatchModel=UserPatchModel
)
user_crud = CrudForgery(
    crud_models=user_crud_models,
    session_factory= authentication.session_factory

)

user_privilege_crud_models = CrudModels(
    entity_name="user_privilege",
    primary_key_name="id",
    SQLAlchemyModel=UserPrivilege,
    CreateModel=UserPrivilegeCreateModel,
    UpdateModel=UserPrivilegeUpdateModel,
    PatchModel=UserPrivilegePatchModel,
)

user_privilege_crud=CrudForgery(
    crud_models=user_privilege_crud_models,
    session_factory=authentication.session_factory
)


