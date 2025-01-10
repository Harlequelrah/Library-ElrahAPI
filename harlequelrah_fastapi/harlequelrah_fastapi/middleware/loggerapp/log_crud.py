from harlequelrah_fastapi.crud.crud_model import CrudForgery
from my_project.settings.secret import authentication
from .log_model import Logger

logCrud = CrudForgery(
    entity_name="log",
    session_factory=authentication.get_session_factory(),
    SQLAlchemyModel=Logger,
)
