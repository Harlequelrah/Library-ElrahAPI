from elrahapi.crud.crud_forgery import CrudForgery
from elrahapi.crud.crud_models import CrudModels
from ..database import database
from .model import LogModel
from .schema import LogReadModel
log_crud_models = CrudModels (
    entity_name='log',
    primary_key_name='id',
    SQLAlchemyModel=LogModel,
    ReadModel=LogReadModel
)
logCrud = CrudForgery(
    crud_models=log_crud_models,
    session_manager= database.session_manager
)
