from typing import Any, List, Optional, Type
from sqlalchemy.ext.asyncio import AsyncSession
from elrahapi.crud.bulk_models import BulkDeleteModel
from elrahapi.crud.crud_models import CrudModels
from elrahapi.database.session_manager import SessionManager
from elrahapi.exception.custom_http_exception import CustomHttpException as CHE
from elrahapi.exception.exceptions_utils import raise_custom_http_exception
from elrahapi.router.router_namespace import TypeRelation
from sqlalchemy.sql import Select
from elrahapi.utility.utils import (
    exec_stmt,
    make_filter,
    map_list_to,
    update_entity,
    validate_value_type,
)
from pydantic import BaseModel
from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from fastapi import status


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

    async def bulk_create(self, create_obj_list:List[BaseModel]):
        session = await self.session_manager.yield_session()
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

    async def create(self, create_obj: Type[BaseModel]):
        if isinstance(create_obj, self.CreatePydanticModel):
            session = await self.session_manager.yield_session()
            dict_obj = create_obj.model_dump()
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
        session = await self.session_manager.yield_session()
        try:
            pk = self.crud_models.get_pk()
            stmt= select(func.count(pk))
            result= await exec_stmt(
                session=session,
                stmt=stmt,
                is_async_env=self.session_manager.is_async_env
            )
            count = result.scalar_one()
            # count = session.query(func.count(pk)).scalar()
            return count
        except Exception as e:
            detail = f"Error occurred while counting {self.entity_name}s , details : {str(e)}"
            raise_custom_http_exception(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
            )

    async def read_all(
        self,
        filter: Optional[str] = None,
        second_model_filter: Optional[str] = None,
        second_model_filter_value: Optional[Any] = None,
        value: Optional[str] = None,
        skip: int = 0,
        limit: int = None,
        relation: Optional["Relationship"] = None,
    ):
        session = await self.session_manager.yield_session()
        stmt = select(self.SQLAlchemyModel)
        pk = self.crud_models.get_pk()
        if relation:
            reskey = relation.get_second_model_key()
            if relation.type_relation == TypeRelation.MANY_TO_MANY_CLASS:
                relkey1 = relation.get_relationship_key1()
                relkey2 = relation.get_relationship_key2()
                stmt = stmt.join(
                    relation.relationship_crud_models.sqlalchemy_model,
                    relkey1 == pk,
                )
                stmt = stmt.join(
                    relation.second_entity_crud_models.sqlalchemy_model,
                    reskey == relkey2,
                )
            elif relation.type_relation in [
                TypeRelation.MANY_TO_MANY_TABLE,
                TypeRelation.ONE_TO_MANY,
            ]:
                stmt = stmt.join(
                    relation.second_entity_crud.crud_models.sqlalchemy_model, reskey=pk
                )
        stmt = make_filter(
            crud_models=self.crud_models, stmt=stmt, filter=filter, value=value
        )
        if relation:
            stmt = make_filter(
                crud_models=relation.second_entity_crud.crud_models,
                stmt=stmt,
                filter=second_model_filter,
                value=second_model_filter_value,
            )
        stmt = stmt.offset(skip).limit(limit)
        results= await exec_stmt(
            stmt=stmt,
            session=session,
            with_scalars=True,
            is_async_env=self.session_manager.is_async_env
        )
        # if self.session_manager.is_async_env:
        #     results= await session.scalars(stmt).all()
        # else:
        #     results= session.scalars(stmt).all()
        return results.all()





    async def read_one(self, pk: Any, db: Optional[Session] = None):
        if db:
            session = db
        else:
            session = await self.session_manager.yield_session()
        pk_attr = self.crud_models.get_pk()
        stmt=select(self.SQLAlchemyModel).where(pk_attr==pk)
        result = await exec_stmt(
            session=session,
            stmt=stmt,
            is_async_env=self.session_manager.is_async_env
        )
        read_obj = result.scalar_one_or_none()
        # read_obj = session.query(self.SQLAlchemyModel).filter(pk_attr == pk).first()
        if read_obj is None:
            detail = f"{self.entity_name} with {self.primary_key_name} {pk} not found"
            raise_custom_http_exception(
                status_code=status.HTTP_404_NOT_FOUND, detail=detail
            )
        return read_obj

    async def update(self, pk: Any, update_obj: Type[BaseModel], is_full_updated: bool):
        session = await self.session_manager.yield_session()
        if (
            isinstance(update_obj, self.UpdatePydanticModel)
            and is_full_updated
            or isinstance(update_obj, self.PatchPydanticModel)
            and not is_full_updated
        ):
            existing_obj = await self.read_one(pk, session)
            try:
                existing_obj = update_entity(
                    existing_entity=existing_obj, update_entity=update_obj
                )
                session.commit()
                session.refresh(existing_obj)
                return existing_obj
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
        session = await self.session_manager.yield_session()
        pk_attr = self.crud_models.get_pk()
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

    async def delete(self, pk: Any):
        session = await self.session_manager.yield_session()
        existing_obj = await self.read_one(pk=pk, db=session)
        try:
            session.delete(existing_obj)
            session.commit()
        except Exception as e:
            session.rollback()
            detail = f"Error occurred while deleting {self.entity_name} with {self.primary_key_name} {pk} , details : {str(e)}"
            raise_custom_http_exception(status.HTTP_500_INTERNAL_SERVER_ERROR, detail)
