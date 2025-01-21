from harlequelrah_fastapi.crud.crud_forgery import CrudForgery
from myproject.settings.database import authentication
from .log_model import Logger

logCrud = CrudForgery(
    entity_name="log",
    SQLAlchemyModel=Logger,
    authentication=authentication,
)
