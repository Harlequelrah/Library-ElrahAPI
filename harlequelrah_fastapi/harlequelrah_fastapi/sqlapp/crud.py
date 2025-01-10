from fastapi.responses import JSONResponse
from sqlalchemy.sql import func
from fastapi import HTTPException, status, Depends, Response
from myproject.myapp.model import SQLAlchemyModel
from myproject.myapp.schema import CreatePydanticModel, UpdatePydanticModel
from sqlalchemy.orm import Session
from harlequelrah_fastapi.utility.utils import update_entity
from harlequelrah_fastapi.crud.crud_model import CrudForgery
from myproject.settings.database import authentication

myapp_crud = CrudForgery(
    entity_name="myapp",
    session_factory=authentication.get_session_factory,
    SQLAlchemyModel=SQLAlchemyModel,
    CreatePydanticModel=CreatePydanticModel,
    UpdatePydanticModel=UpdatePydanticModel,
)
