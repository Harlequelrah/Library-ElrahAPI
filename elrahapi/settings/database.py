from elrahapi.database.database_manager import DatabaseManager
from sqlalchemy.orm import declarative_base

from .secret import (
    DATABASE,
    DATABASE_ASYNC_CONNECTOR,
    DATABASE_CONNECTOR,
    DATABASE_NAME,
    DATABASE_PASSWORD,
    DATABASE_SERVER,
    DATABASE_USERNAME,
    IS_ASYNC_ENV,
)

database = DatabaseManager(
    database=DATABASE,
    database_username=DATABASE_USERNAME,
    database_password=DATABASE_PASSWORD,
    database_connector=DATABASE_CONNECTOR,
    database_async_connector=DATABASE_ASYNC_CONNECTOR,
    database_name=DATABASE_NAME,
    database_server=DATABASE_SERVER,
    is_async_env=IS_ASYNC_ENV,
)

try:
    database.create_database_if_not_exists()
finally:
    database.create_session_manager()
    Base = declarative_base()
