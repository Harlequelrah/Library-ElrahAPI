from harlequelrah_fastapi.crud.crud_forgery import CrudForgery
from my_project.settings.secret import authentication
from .log_model import Logger

logCrud = CrudForgery(
    entity_name="log",
    SQLAlchemyModel=Logger,
    authentication=authentication,
)
