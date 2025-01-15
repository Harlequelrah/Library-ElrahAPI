from sqlalchemy import create_engine, text

def update_entity(existing_entity, update_entity):
    for key, value in update_entity.dict().items():
        if value is not None and hasattr(existing_entity, key):
            setattr(existing_entity, key, value)
    return existing_entity


async def validate_value_type(value):
    if value in ["true", "True"]:
        value = True
    elif value in ["false", "False"]:
        value = False
    elif value.isdigit():
        value = int(value)
    else : value = str(value)
    return value


def create_database_if_not_exists(database_url:str, database_name:str):
    engine = create_engine(database_url, pool_pre_ping=True)
    conn = engine.connect()
    try:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {database_name}"))
    finally:
        conn.close()
