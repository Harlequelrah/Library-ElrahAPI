from typing import Any, List, Optional, Type
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from elrahapi.crud.crud_models import CrudModels
import os
from sqlalchemy.sql import Select
from elrahapi.utility.types import ElrahSession


def map_list_to(
    obj_list: List[BaseModel],
    obj_sqlalchemy_class: type,
    obj_pydantic_class: Type[BaseModel],
):
    return [
        obj_sqlalchemy_class(**obj.model_dump())
        for obj in obj_list
        if isinstance(obj, obj_pydantic_class)
    ]


def update_entity(existing_entity, update_entity: Type[BaseModel]):
    validate_update_entity = update_entity.model_dump(exclude_unset=True)
    for key, value in validate_update_entity.items():
        if value is not None and hasattr(existing_entity, key):
            setattr(existing_entity, key, value)
    return existing_entity


def validate_value(value: Any):
    if value is None:
        return None
    elif value.lower() == "true":
        value = True
    elif value.lower() == "false":
        value = False
    elif value.isdigit():
        value = int(value)
    else:
        try:
            value = float(value)
        except ValueError:
            value = str(value)
    return value


def make_filter(
    stmt: Select,
    crud_models: CrudModels,
    filter: Optional[str] = None,
    value: Optional[str] = None,
) -> Select:
    if filter and value:
        exist_filter = crud_models.get_attr(filter)
        validated_value = validate_value(value)
        stmt = stmt.where(exist_filter == validated_value)
    return stmt


def get_env_int(env_key: str):
    number = os.getenv(env_key)
    if number is None:
        return number
    else:
        if number.isdigit():
            return number

def is_async_session(session:ElrahSession):
    return isinstance(session,AsyncSession)

async def exec_stmt(
    stmt: Select,
    session: ElrahSession,
    with_scalars: bool = False

):
    if isinstance(session,AsyncSession):
        if with_scalars:
            result=await session.scalars(stmt)
            return result.unique() if result else None
        else:
            result= await session.execute(stmt)
            return result.unique() if result else None
    else:
        if with_scalars:
            return session.scalars(stmt)
        else:
            return session.execute(stmt)
