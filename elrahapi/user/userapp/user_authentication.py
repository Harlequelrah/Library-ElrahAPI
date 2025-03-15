from elrahapi.authentication.authentication_manager import AuthenticationManager
from elrahapi.crud.crud_models import CrudModels
from myproject.settings.database import authentication_provider
from .user_models import User
from .user_schemas import UserPydanticModel,UserCreateModel,UserUpdateModel,UserPatchModel
user_crud_models = CrudModels(
    entity_name="user",
    primary_key="id",
    SQLAlchemyModel=User,
    PydanticModel=UserPydanticModel,
    CreateModel= UserCreateModel,
    PatchModel=UserPatchModel,
    UpdateModel=UserUpdateModel,
)

user_authentication = AuthenticationManager(
    authentication_provider=authentication_provider,
    crud_models = user_crud_models

)
