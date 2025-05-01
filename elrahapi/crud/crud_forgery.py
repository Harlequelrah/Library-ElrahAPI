from typing import Optional, Type
from elrahapi.crud.bulk_models import BulkDeleteModel
from elrahapi.crud.crud_models import CrudModels
from elrahapi.exception.custom_http_exception import CustomHttpException as CHE
from elrahapi.exception.exceptions_utils import raise_custom_http_exception
from elrahapi.session.session_manager import SessionManager
from elrahapi.utility.utils import map_list_to, update_entity, validate_value_type
from sqlalchemy import delete, func
from sqlalchemy.orm import Session

from fastapi import status

from elrahapi.router.model_relation import ModelRelation


class CrudForgery:
    def __init__(self, session_manager: SessionManager, crud_models: CrudModels):
        self.crud_models = crud_models
        self.entity_name = crud_models.entity_name
        self.ReadPydanticModel = crud_models.read_model
        self.FullReadPydanticModel = crud_models.full_read_model
        self.SQLAlchemyModel = crud_models.sqlalchemy_model
        self.CreatePydanticModel = crud_models.create_model
        self.UpdatePydanticModel = crud_models.update_model
        self.PatchPydanticModel = crud_models.patch_model
        self.primary_key_name = crud_models.primary_key_name
        self.session_manager = session_manager

    async def bulk_create(self, create_obj_list: list):
        session = self.session_manager.yield_session()
        try:
            create_list = map_list_to(
                create_obj_list, self.SQLAlchemyModel, self.CreatePydanticModel
            )
            if len(create_list) != len(create_obj_list):
                detail = f"Invalid {self.entity_name}s  object for bulk creation"
                raise_custom_http_exception(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=detail
                )
            session.add_all(create_list)
            session.commit()
            for create_obj in create_list:
                session.refresh(create_obj)
            return create_list
        except Exception as e:
            session.rollback()
            detail = f"Error occurred while bulk creating {self.entity_name} , details : {str(e)}"
            raise_custom_http_exception(
                status_code=status.HTTP_400_BAD_REQUEST, detail=detail
            )

    async def create(self, create_obj):
        if isinstance(create_obj, self.CreatePydanticModel):
            session = self.session_manager.yield_session()
            dict_obj = create_obj.dict()
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
        session = self.session_manager.yield_session()
        try:
            pk = await self.crud_models.get_pk()
            count = session.query(func.count(pk)).scalar()
            return count
        except Exception as e:
            detail = f"Error occurred while counting {self.entity_name}s , details : {str(e)}"
            raise_custom_http_exception(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
            )

    async def read_all(
        self,
        filter: Optional[str] = None,
        result_filter: Optional[str] = None,
        result_filter_value: Optional[str] = None,
        value=None,
        skip: int = 0,
        limit: int = None,
        relation: Optional[ModelRelation] = None,
    ):
        session = self.session_manager.yield_session()
        query = session.query(self.SQLAlchemyModel)
        pk = await self.crud_models.get_pk()
        if relation :
            relkey1 = await relation.get_relationship_key1()
            relkey2 = await relation.get_relationship_key2()
            reskey = await relation.get_result_model_key()
            query=query.join(
                relation.relationship_crud_models.sqlalchemy_model,
                relkey1 == pk,
            )
            query = query.join(
                relation.result_crud_models.sqlalchemy_model,
                reskey == relkey2,
            )
        if filter and value:
            exist_filter = await self.crud_models.get_attr(filter)
            validated_value = await validate_value_type(value)
            query = query.filter(exist_filter == validated_value)
        if result_filter and result_filter_value:
            exist_filter = await relation.result_crud_models.get_attr(result_filter)
            validated_value = await validate_value_type(result_filter_value)
            query = query.filter(exist_filter == validated_value)
        results = query.offset(skip).limit(limit).all()
        return results

    async def read_one(self, pk, db: Optional[Session] = None):
        if db:
            session = db
        else:
            session = self.session_manager.yield_session()
        pk_attr = await self.crud_models.get_pk()
        read_obj = session.query(self.SQLAlchemyModel).filter(pk_attr == pk).first()
        if read_obj is None:
            detail = f"{self.entity_name} with {self.primary_key_name} {pk} not found"
            raise_custom_http_exception(
                status_code=status.HTTP_404_NOT_FOUND, detail=detail
            )
        return read_obj

    async def update(self, pk, update_obj, is_full_updated: bool):
        session = self.session_manager.yield_session()
        if (
            isinstance(update_obj, self.UpdatePydanticModel)
            and is_full_updated
            or isinstance(update_obj, self.PatchPydanticModel)
            and not is_full_updated
        ):
            try:
                existing_obj = await self.read_one(pk, session)
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
                    detail = f"Error occurred while updating {self.entity_name} with {self.primary_key_name} {pk} , details : {http_exc.detail}"
                    raise_custom_http_exception(
                        status_code=status.HTTP_404_NOT_FOUND, detail=detail
                    )
            except Exception as e:
                session.rollback()
                detail = f"Error occurred while updating {self.entity_name} with {self.primary_key_name} {pk} , details : {str(e)}"
                raise_custom_http_exception(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
                )
        else:
            detail = f"Invalid {self.entity_name}  object for update"
            raise_custom_http_exception(
                status_code=status.HTTP_400_BAD_REQUEST, detail=detail
            )

    async def bulk_delete(self, pk_list: BulkDeleteModel):
        session = self.session_manager.yield_session()
        pk_attr = await self.crud_models.get_pk()
        delete_list = pk_list.delete_liste
        try:
            session.execute(
                delete(self.SQLAlchemyModel).where(pk_attr.in_(delete_list))
            )
            session.commit()
        except Exception as e:
            session.rollback()
            detail = f"Error occurred while bulk deleting {self.entity_name}s , details : {str(e)}"
            raise_custom_http_exception(status.HTTP_500_INTERNAL_SERVER_ERROR, detail)

    async def delete(self, pk):
        session = self.session_manager.yield_session()
        try:
            existing_obj = await self.read_one(pk=pk, db=session)
            session.delete(existing_obj)
            session.commit()
        except CHE as che:
            session.rollback()
            http_exc = che.http_exception
            if http_exc.status_code == status.HTTP_404_NOT_FOUND:
                detail = f"Error occurred while deleting {self.entity_name} with {self.primary_key_name} {pk} , details : {http_exc.detail}"
                raise_custom_http_exception(status.HTTP_404_NOT_FOUND, detail)
        except Exception as e:
            session.rollback()
            detail = f"Error occurred while deleting {self.entity_name} with {self.primary_key_name} {pk} , details : {str(e)}"
            raise_custom_http_exception(status.HTTP_500_INTERNAL_SERVER_ERROR, detail)
