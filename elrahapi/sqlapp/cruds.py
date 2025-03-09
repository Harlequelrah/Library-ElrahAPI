from myproject.myapp.models import SQLAlchemyModel # remplacer SQLAlchemy
from myproject.myapp.schemas import EntityCreateModel, EntityUpdateModel,EntityPatchModel
from elrahapi.crud.crud_forgery import CrudForgery
from myproject.settings.database import authentication

myapp_crud = CrudForgery(
    entity_name="myapp",
    primary_key_name="id",  #remplacer au besoin par le nom de la clé primaire
    authentication=authentication,
    SQLAlchemyModel=SQLAlchemyModel,
    CreatePydanticModel=EntityCreateModel, #Optionel
    UpdatePydanticModel=EntityUpdateModel, #Optionel
    PatchPydanticModel=EntityPatchModel #Optionel
)
