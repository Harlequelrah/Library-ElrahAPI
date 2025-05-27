from typing import Any, List, Optional, Type
from elrahapi.exception.custom_http_exception import CustomHttpException
from elrahapi.crud.bulk_models import BulkDeleteModel
from elrahapi.crud.crud_models import CrudModels
from elrahapi.exception.exceptions_utils import raise_custom_http_exception
from elrahapi.router.router_namespace import TypeRelation
from elrahapi.utility.types import ElrahSession
from elrahapi.utility.utils import (
    exec_stmt,
    is_async_session,
    make_filter,
    map_list_to,
    update_entity,
)
from pydantic import BaseModel
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from fastapi import status

from elrahapi.database.session_manager import SessionManager

from elrahapi.crud.base_crud_forgery import BaseCrudForgery


class CrudForgery(BaseCrudForgery):
    def __init__(
        self,
        crud_models: CrudModels,
        session_manager:SessionManager
    ):
        super().__init__(crud_models=crud_models, session_manager=session_manager)

    async def bulk_create(
        self,  create_obj_list: List[BaseModel]
    ):
        try:
            session:ElrahSession = await self.session_manager.get_session()
            return await super().bulk_create(
                session=session,
                create_obj_list=create_obj_list
                )
        except Exception as e:
            await self.session_manager.rollback_session(session=session)
            detail = f"Error occurred while bulk creating {self.entity_name} , details : {str(e)}"
            raise_custom_http_exception(
                status_code=status.HTTP_400_BAD_REQUEST, detail=detail
            )
        finally:
            await self.session_manager.close_session(session=session)

    async def create(self,create_obj: Type[BaseModel]):
        if isinstance(create_obj, self.CreatePydanticModel):
            try:
                session :ElrahSession = await self.session_manager.get_session()
                return await super().create(
                    session=session,
                    create_obj=create_obj
                )
            except Exception as e:
                await self.session_manager.rollback_session(session=session)
                detail = f"Error occurred while creating {self.entity_name} , details : {str(e)}"
                raise_custom_http_exception(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=detail
                )
            finally :
                await self.session_manager.close_session(session=session)
        else:
            detail = f"Invalid {self.entity_name} object for creation"
            raise_custom_http_exception(
                status_code=status.HTTP_400_BAD_REQUEST, detail=detail
            )


    async def count(
        self,
    ) -> int:
        try:
            session:ElrahSession = await self.session_manager.get_session()
            return await super().count(
                session=session
                )
        except Exception as e:
            await self.session_manager.rollback_session(session=session)
            detail = f"Error occurred while counting {self.entity_name}s , details : {str(e)}"
            raise_custom_http_exception(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
            )
        finally :
            await self.session_manager.close_session(session=session)

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
        try :
            session: ElrahSession = await self.session_manager.get_session()
            return await super().read_all(
                session=session,
                filter=filter,
                second_model_filter=second_model_filter,
                second_model_filter_value=second_model_filter_value,
                value=value,
                skip=skip,
                limit=limit,
                relation=relation,
            )
        except Exception as e:
            await self.session_manager.rollback_session(session=session)
            detail = f"Error occurred while reading all {self.entity_name}s , details : {str(e)}"
            raise_custom_http_exception(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
            )
        finally:
            await self.session_manager.close_session(session=session)

    async def read_one(self, pk: Any):
        try:
            session: ElrahSession = await self.session_manager.get_session()
            return await super().read_one(
                session=session,
                pk=pk
            )
        except CustomHttpException as che:
            await self.session_manager.rollback_session(session=session)
            raise che
        except Exception as e:
            await self.session_manager.rollback_session(session=session)
            detail = f"Error occurred while reading {self.entity_name} with {self.primary_key_name} {pk} , details : {str(e)}"
            raise_custom_http_exception(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
            )
        finally:
            await self.session_manager.close_session(session=session)

    async def update(
        self,
        pk: Any,
        update_obj: Type[BaseModel],
        is_full_update: bool,
    ):
        if (
            isinstance(update_obj, self.UpdatePydanticModel)
            and is_full_update
            or isinstance(update_obj, self.PatchPydanticModel)
            and not is_full_update
        ):
            try:
                session: ElrahSession = await self.session_manager.get_session()
                existing_obj = await super().read_one(pk=pk, session=session)
                return await super().update(
                    session=session,
                    pk=pk,
                    existing_obj=existing_obj,
                    update_obj=update_obj,
                )
            except Exception as e:
                await self.session_manager.rollback_session(session=session)
                detail = f"Error occurred while updating {self.entity_name} with {self.primary_key_name} {pk} , details : {str(e)}"
                raise_custom_http_exception(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
                )
            finally:
                await self.session_manager.close_session(session=session)
        else:
            detail = f"Invalid {self.entity_name}  object for update"
            raise_custom_http_exception(
                status_code=status.HTTP_400_BAD_REQUEST, detail=detail
            )

    async def bulk_delete(self, session: ElrahSession, pk_list: BulkDeleteModel):
        pk_attr = self.crud_models.get_pk()
        delete_list = pk_list.delete_liste
        try:
            if is_async_session(session):
                await session.execute(
                    delete(self.SQLAlchemyModel).where(pk_attr.in_(delete_list))
                )
                await session.commit()
            else:
                session.execute(
                    delete(self.SQLAlchemyModel).where(pk_attr.in_(delete_list))
                )
                session.commit()
        except Exception as e:
            if is_async_session(session):
                await session.rollback()
            else:
                session.rollback()
            detail = f"Error occurred while bulk deleting {self.entity_name}s , details : {str(e)}"
            raise_custom_http_exception(status.HTTP_500_INTERNAL_SERVER_ERROR, detail)

    async def delete(self, session: ElrahSession, pk: Any):
        existing_obj = await self.read_one(pk=pk, session=session)
        try:
            if is_async_session(session):
                await session.delete(existing_obj)
                await session.commit()
            else:
                session.delete(existing_obj)
                session.commit()
        except Exception as e:
            if is_async_session(session):
                await session.rollback()
            else:
                session.rollback()
            detail = f"Error occurred while deleting {self.entity_name} with {self.primary_key_name} {pk} , details : {str(e)}"
            raise_custom_http_exception(status.HTTP_500_INTERNAL_SERVER_ERROR, detail)
