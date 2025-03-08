from elrahapi.crud.crud_forgery import CrudForgery
from myproject.settings.database import authentication
from .log_model import Logger

logCrud = CrudForgery(
    entity_name="log",
    primary_key_name="id",
    SQLAlchemyModel=Logger,
    authentication=authentication,
)
