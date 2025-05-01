from sqlalchemy import create_engine, text
from typing import Any

def map_list_to(obj_list: list,obj_sqlalchemy_class:type, obj_pydantic_class: type):
    return [obj_sqlalchemy_class(**obj.dict()) for obj in obj_list if isinstance(obj,obj_pydantic_class)]

def update_entity(existing_entity, update_entity):
    validate_update_entity=update_entity.dict(exclude_unset=True)
    for key, value in validate_update_entity.items():
        if value is not None and hasattr(existing_entity, key):
            setattr(existing_entity, key, value)
    return existing_entity


async def validate_value_type(value:Any):
    if value is None:
        return None
    elif value.lower()=="true":
        value = True
    elif value.lower() == "false":
        value = False
    elif value.isdigit():
        value = int(value)
    else:
        try :
            value = float(value)
        except ValueError:
            value=str(value)
    return value


def create_database_if_not_exists(database_url:str, database_name:str):
    engine = create_engine(database_url, pool_pre_ping=True)
    conn = engine.connect()
    try:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {database_name}"))
    finally:
        conn.close()


