from elrahapi.crud.crud_forgery import CrudForgery
from elrahapi.crud.crud_models import CrudModels
from ..auth.configs import authentication
from .model import Logger
from .schema import LogPydanticModel
log_crud_models = CrudModels (
    entity_name='log',
    primary_key_name='id',
    SQLAlchemyModel=Logger,
    PydanticModel=LogPydanticModel
)
logCrud = CrudForgery(
    session_factory= authentication.session_factory,
    crud_models=log_crud_models
)
