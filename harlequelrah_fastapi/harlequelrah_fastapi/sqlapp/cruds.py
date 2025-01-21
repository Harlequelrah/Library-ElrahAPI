from myproject.myapp.models import SQLAlchemyModel
from myproject.myapp.schemas import CreatePydanticModel, UpdatePydanticModel
from harlequelrah_fastapi.crud.crud_forgery import CrudForgery
from myproject.settings.database import authentication

myapp_crud = CrudForgery(
    entity_name="myapp",
    session_factory=authentication.session_factory,
    SQLAlchemyModel=SQLAlchemyModel,
    CreatePydanticModel=CreatePydanticModel,
    UpdatePydanticModel=UpdatePydanticModel,
)
