from elrahapi.crud.crud_models import CrudModels
from myproject.myapp.models import Entity  #remplacer par l'entité SQLAlchemy
from myproject.myapp.schemas import EntityCreateModel, EntityUpdateModel,EntityPatchModel,EntityPydanticModel
from elrahapi.crud.crud_forgery import CrudForgery
from myproject.settings.database import authentication


myapp_crud_models = CrudModels(
    entity_name="myapp",
    primary_key_name="id",  #remplacer au besoin par le nom de la clé primaire
    SQLAlchemyModel=Entity, #remplacer par l'entité SQLAlchemy
    CreateModel=EntityCreateModel, #Optionel
    UpdateModel=EntityUpdateModel, #Optionel
    PatchModel=EntityPatchModel, #Optionel
    PydanticModel=EntityPydanticModel, #Optionel
)
myapp_crud = CrudForgery(
    crud_models=myapp_crud_models,
    session_factory= authentication.session_factory

)
