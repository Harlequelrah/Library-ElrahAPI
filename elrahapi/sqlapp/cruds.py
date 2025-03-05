from myproject.myapp.models import SQLAlchemyModel
from myproject.myapp.schemas import EntityCreateModel, EntityUpdateModel,EntityPatchModel
from elrahapi.crud.crud_forgery import CrudForgery
from myproject.settings.database import authentication

myapp_crud = CrudForgery(
    entity_name="myapp",
    primary_key_name="id",
    authentication=authentication,
    SQLAlchemyModel=SQLAlchemyModel,
    CreatePydanticModel=EntityCreateModel,
    UpdatePydanticModel=EntityUpdateModel,
    PatchPydanticModel=EntityPatchModel
)
