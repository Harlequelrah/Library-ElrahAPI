from elrahapi.crud.crud_forgery import CrudForgery
from elrahapi.crud.crud_models import CrudModels
from myproject.myapp.models import Entity  # remplacer par l'entité SQLAlchemy
from myproject.myapp.schemas import (  # remplacer par les modèles Pydantic
    EntityCreateModel,
    EntityFullReadModel,
    EntityPatchModel,
    EntityReadModel,
    EntityUpdateModel,
)
from myproject.settings.database import database_manager

myapp_crud_models = CrudModels(
    entity_name="myapp",
    primary_key_name="id",  # remplacer au besoin par le nom de la clé primaire
    SQLAlchemyModel=Entity,  # remplacer par l'entité SQLAlchemy
    ReadModel=EntityReadModel,
    CreateModel=EntityCreateModel,  # Optionel
    UpdateModel=EntityUpdateModel,  # Optionel
    PatchModel=EntityPatchModel,  # Optionel
    FullReadModel=EntityFullReadModel,  # Optionel
)
myapp_crud = CrudForgery(
    crud_models=myapp_crud_models, session_manager=database_manager.session_manager
)
