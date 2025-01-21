from typing import List, Optional
from fastapi.responses import JSONResponse
from harlequelrah_fastapi.authentication.authenticate import Authentication
from harlequelrah_fastapi.crud.link_class import LinkClass, manage_linked_classes
from harlequelrah_fastapi.exception.custom_http_exception import (
    CustomHttpException as CHE,
)
from fastapi import HTTPException as HE, Response, status
from harlequelrah_fastapi.exception.exceptions_utils import raise_custom_http_exception
from harlequelrah_fastapi.utility.utils import update_entity, validate_value_type
from sqlalchemy import func
from sqlalchemy.orm import Session, sessionmaker


class CrudForgery:
    def __init__(
        self,
        entity_name: str,
        authentication: Authentication,
        SQLAlchemyModel,
        CreatePydanticModel=None,
        UpdatePydanticModel=None,
        Linked_Classes: List[LinkClass] = [],
    ):
        self.SQLAlchemyModel = SQLAlchemyModel
        self.CreatePydanticModel = CreatePydanticModel
        self.UpdatePydanticModel = UpdatePydanticModel
        self.entity_name = entity_name
        self.authentication = authentication
        self.session_factory = authentication.session_factory
        self.Linked_Classes = Linked_Classes

    async def create(self, create_obj):
        if isinstance(create_obj, self.CreatePydanticModel):
            session = self.session_factory()
            dict_obj = create_obj.dict()
            if self.Linked_Classes:
                dict_obj = await manage_linked_classes(self.Linked_Classes)

            new_obj = self.SQLAlchemyModel(**dict_obj)
            try:
                session.add(new_obj)
                session.commit()
                session.refresh(new_obj)
                return new_obj
            except Exception as e:
                session.rollback()
                detail = f"Error occurred while creating {self.entity_name} , details : {str(e)}"
                raise_custom_http_exception(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=detail
                )
        else:
            detail = f"Invalid {self.entity_name} object for creation"
            raise_custom_http_exception(
                status_code=status.HTTP_400_BAD_REQUEST, detail=detail
            )

    async def count(self) -> int:
        session = self.session_factory()
        try:
            count = session.query(func.count(self.SQLAlchemyModel.id)).scalar()
            return count
        except Exception as e:
            detail = f"Error occurred while counting {self.entity_name}s , details : {str(e)}"
            raise_custom_http_exception(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
            )

    async def read_all(self, skip: int = 0, limit: int = None):
        session = self.session_factory()
        return session.query(self.SQLAlchemyModel).offset(skip).limit(limit).all()

    async def read_all_by_filter(self, filter, value, skip: int = 0, limit: int = None):
        session = self.session_factory()
        exist_filter = getattr(self.SQLAlchemyModel, filter, None)
        if exist_filter:
            value = await validate_value_type(value)
            return (
                session.query(self.SQLAlchemyModel)
                .filter(exist_filter == value)
                .offset(skip)
                .limit(limit)
                .all()
            )
        else:
            detail = f"Invalid filter {filter} for entity {self.entity_name}"
            raise_custom_http_exception(
                status_code=status.HTTP_400_BAD_REQUEST, detail=detail
            )

    async def read_one(self, id: int, db: Optional[Session] = None):
        if db:
            session = db
        else:
            session = self.session_factory()
        read_obj = (
            session.query(self.SQLAlchemyModel)
            .filter(self.SQLAlchemyModel.id == id)
            .first()
        )
        if read_obj is None:
            detail = f"{self.entity_name} with id {id} not found"
            raise_custom_http_exception(
                status_code=status.HTTP_404_NOT_FOUND, detail=detail
            )
        return read_obj

    async def update(self, id: int, update_obj):
        if isinstance(update_obj, self.UpdatePydanticModel):
            session = self.session_factory()
            try:
                existing_obj = await self.read_one(id, session)
                existing_obj = update_entity(
                    existing_entity=existing_obj, update_entity=update_obj
                )
                session.commit()
                session.refresh(existing_obj)
                return existing_obj
            except CHE as che:
                session.rollback()
                http_exc = che.http_exception
                if http_exc.status_code == status.HTTP_404_NOT_FOUND:
                    detail = f"Error occurred while updating {self.entity_name} with id {id} , details : {http_exc.detail}"
                    raise_custom_http_exception(
                        status_code=status.HTTP_404_NOT_FOUND, detail=detail
                    )
            except Exception as e:
                session.rollback()
                detail = f"Error occurred while updating {self.entity_name} with id {id} , details : {str(e)}"
                raise_custom_http_exception(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
                )
        else:
            detail = f"Invalid {self.entity_name}  object for update"
            raise_custom_http_exception(
                status_code=status.HTTP_400_BAD_REQUEST, detail=detail
            )

    async def delete(self, id):
        session = self.session_factory()
        try:
            existing_obj = await self.read_one(id=id, db=session)
            session.delete(existing_obj)
            session.commit()
        except CHE as che:
            session.rollback()
            http_exc = che.http_exception
            if http_exc.status_code == status.HTTP_404_NOT_FOUND:
                detail = f"Error occurred while deleting {self.entity_name} with id {id} , details : {http_exc.detail}"
                raise_custom_http_exception(status.HTTP_404_NOT_FOUND, detail)
        except Exception as e:
            session.rollback()
            detail = f"Error occurred while deleting {self.entity_name} with id {id} , details : {str(e)}"
            raise_custom_http_exception(status.HTTP_500_INTERNAL_SERVER_ERROR, detail)
