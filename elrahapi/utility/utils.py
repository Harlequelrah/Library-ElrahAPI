
import os
from typing import Any, Type
from datetime import datetime
from elrahapi.authorization.privilege.schemas import PrivilegeCreateModel
from elrahapi.crud.crud_models import CrudModels
from elrahapi.router.router_routes_name import CREATE_ALL_PRIVILEGE_ROUTES_NAME
from elrahapi.utility.types import ElrahSession
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from fastapi import Request


def map_list_to(
    obj_list: list[BaseModel],
    obj_sqlalchemy_class: type,
    obj_pydantic_class: Type[BaseModel],
):
    try:
        if not obj_list:
            return []
        return [
            obj_sqlalchemy_class(**obj.model_dump())
            for obj in obj_list
            if isinstance(obj, obj_pydantic_class)
        ]
    except Exception as e:
        raise ValueError(f"Error mapping list to SQLAlchemy class: {e}") from e


def update_entity(existing_entity, update_entity: Type[BaseModel]):
    validate_update_entity = update_entity.model_dump(exclude_unset=True)
    for key, value in validate_update_entity.items():
        if value is not None and hasattr(existing_entity, key):
            setattr(existing_entity, key, value)
    return existing_entity


def validate_value(value: Any):
    if isinstance(value, str):
        if value.lower() == "true":
            value = True
        elif value.lower() == "false":
            value = False
        elif value.isdigit():
            return int(value)
    else:
        try:
            value = float(value)
        except (ValueError, TypeError):
            value = str(value)
    return value


def get_pks(l: list, pk_name: str):
    pk_list = []
    for i in l:
        pk = getattr(i, pk_name)
        pk_list.append(pk)
    return pk_list


def apply_filters(
    stmt: Select,
    crud_models: CrudModels,
    filters: dict[str, Any],
) -> Select:
    conditions = [
        crud_models.get_attr(f) == validate_value(v)
        for f, v in filters.items()
        if hasattr(crud_models.sqlalchemy_model, f)
    ]
    stmt = stmt.where(*conditions)
    return stmt


async def exec_stmt(
    stmt: Select,
    session: ElrahSession,
    with_scalars: bool = False,
    with_scalar: bool = False,
):
    if isinstance(session, AsyncSession):
        if with_scalars:
            result = await session.scalars(stmt)
        elif with_scalar:
            result = await session.scalar(stmt)
        else:
            result = await session.execute(stmt)
    else:
        if with_scalars:
            result = session.scalars(stmt)
        elif with_scalar:
            result = session.scalar(stmt)
        else:
            result = session.execute(stmt)
    return result


def get_filters(request: Request):
    filters = dict(request.query_params)
    filters.pop("skip", None)
    filters.pop("limit", None)
    return filters


def get_entities_all_privilege_data(entities_names: list[str]) -> list[BaseModel]:
    privileges: list[PrivilegeCreateModel] = []
    operations = [op.value.upper() for op in CREATE_ALL_PRIVILEGE_ROUTES_NAME]
    for entity_name in entities_names:
        for operation in operations:
            privilege = PrivilegeCreateModel(
                name=f"CAN {operation} {entity_name}",
                description=f"{entity_name} {operation.lower()} privilege",
                is_active=True,
            )
            privileges.append(privilege)
    return privileges

def update_expected_value_dates(expected_value: dict) -> dict:
        current_date = datetime.now().replace(microsecond=0).isoformat()
        expected_value.update(
            {
                "date_created": current_date,
                "date_updated": current_date,
            }
        )
        return expected_value

def exclude_dates_from_json(expected_value: dict) -> dict:
    expected_value.pop("date_created", None)
    expected_value.pop("date_updated", None)
    return expected_value
