from typing import Any, Type
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from elrahapi.authorization.privilege.schemas import PrivilegeCreateModel
from elrahapi.crud.crud_models import CrudModels
import os
from sqlalchemy.sql import Select
from elrahapi.router.router_routes_name import CREATE_ALL_PRIVILEGE_ROUTES_NAME
from elrahapi.utility.types import ElrahSession


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
        # print(f"Error mapping list to SQLAlchemy class: {e}")


def update_entity(existing_entity, update_entity: Type[BaseModel]):
    validate_update_entity = update_entity.model_dump(exclude_unset=True)
    for key, value in validate_update_entity.items():
        if value is not None and hasattr(existing_entity, key):
            setattr(existing_entity, key, value)
    return existing_entity


def validate_value(value: Any):
    if value is None:
        return None
    elif isinstance(value, bool):
        return value
    elif value.lower() == "true" :
        value = True
    elif value.lower() == "false" :
        value = False
    elif value.isdigit():
        value = int(value)
    else:
        try:
            value = float(value)
        except ValueError:
            value = str(value)
    return value

def get_pks(l : list,pk_name:str):
    pk_list = []
    for i in l :
        pk = getattr(i,pk_name)
        pk_list.append(pk)
    return pk_list


def make_filter(
    stmt: Select,
    crud_models: CrudModels,
    filter: str | None = None,
    value: str | None = None,
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


def get_entities_all_privilege_data(entities_names:list[str]) -> list[BaseModel]:
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
