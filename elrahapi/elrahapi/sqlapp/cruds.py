from myproject.myapp.models import SQLAlchemyModel
from myproject.myapp.schemas import CreatePydanticModel, UpdatePydanticModel
from elrahapi.crud.crud_forgery import CrudForgery
from myproject.settings.database import authentication

myapp_crud = CrudForgery(
    entity_name="myapp",
    authentication=authentication,
    SQLAlchemyModel=SQLAlchemyModel,
    CreatePydanticModel=EntityCreatePydanticModel,
    UpdatePydanticModel=EntityUpdatePydanticModel,
)
