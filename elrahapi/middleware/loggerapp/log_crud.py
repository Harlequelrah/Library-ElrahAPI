from elrahapi.crud.crud_forgery import CrudForgery
from elrahapi.crud.crud_models import CrudModels
from myproject.settings.database import authentication_provider
from .log_model import Logger
from .log_schema import LogPydanticModel
log_crud_models = CrudModels (
    entity_name='log',
    primary_key_name='id',
    SQLAlchemyModel=Logger,
    PydanticModel=LogPydanticModel
)
logCrud = CrudForgery(
    session_factory= authentication_provider.session_factory,
    crud_models=log_crud_models
)
