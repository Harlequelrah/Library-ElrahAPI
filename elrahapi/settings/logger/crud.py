from app.settings.config.database_config import session_manager
from app.settings.logger.model import LogModel
from app.settings.logger.schema import LogReadModel
from elrahapi.crud.crud_forgery import CrudForgery
from elrahapi.crud.crud_models import CrudModels

log_crud_models = CrudModels(
    entity_name="log",
    primary_key_name="id",
    SQLAlchemyModel=LogModel,
    ReadModel=LogReadModel,
)
logCrud = CrudForgery(crud_models=log_crud_models, session_manager=session_manager)
