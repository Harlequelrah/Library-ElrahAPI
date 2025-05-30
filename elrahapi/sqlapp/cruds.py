from elrahapi.crud.crud_models import CrudModels
from .models import Entity  #remplacer par l'entité SQLAlchemy
from .schemas import EntityCreateModel, EntityUpdateModel,EntityPatchModel,EntityReadModel,EntityFullReadModel #remplacer par les modèles Pydantic
from elrahapi.crud.crud_forgery import CrudForgery
from ..settings.database import database

myapp_crud_models = CrudModels(
    entity_name="myapp",
    primary_key_name="id",  #remplacer au besoin par le nom de la clé primaire
    SQLAlchemyModel=Entity, #remplacer par l'entité SQLAlchemy
    ReadModel=EntityReadModel,
    CreateModel=EntityCreateModel, #Optionel
    UpdateModel=EntityUpdateModel, #Optionel
    PatchModel=EntityPatchModel, #Optionel
    FullReadModel=EntityFullReadModel #Optionel
)
myapp_crud = CrudForgery(
    crud_models=myapp_crud_models,
    session_manager=database.session_manager
)
