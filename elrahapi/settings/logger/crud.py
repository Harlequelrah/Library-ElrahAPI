from elrahapi.crud.crud_forgery import CrudForgery
from elrahapi.crud.crud_models import CrudModels
from myproject.settings.config.database_config import session_manager
from myproject.settings.logger.model import LogModel
from myproject.settings.logger.schema import LogReadModel

log_crud_models = CrudModels(
    entity_name="log",
    primary_key_name="id",
    SQLAlchemyModel=LogModel,
    ReadModel=LogReadModel,
)
logCrud = CrudForgery(
    crud_models=log_crud_models, session_manager=session_manager
)
