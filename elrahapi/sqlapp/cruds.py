from elrahapi.crud.crud_models import CrudModels
from myproject.myapp.models import SQLAlchemyModel # remplacer SQLAlchemy
from myproject.myapp.schemas import EntityCreateModel, EntityUpdateModel,EntityPatchModel
from elrahapi.crud.crud_forgery import CrudForgery
from myproject.settings.database import authentication_provider


myapp_crud_models = CrudModels(
    entity_name="myapp",
    primary_key_name="id",  #remplacer au besoin par le nom de la clé primaire
    SQLAlchemyModel=SQLAlchemyModel, #remplacer par l'entité SQLAlchemy
    CreateModel=EntityCreateModel, #Optionel
    UpdateModel=EntityUpdateModel, #Optionel
    PatchModel=EntityPatchModel #Optionel
)
myapp_crud = CrudForgery(
    crud_models=myapp_crud_models,
    session_factory= authentication_provider.session_factory

)
