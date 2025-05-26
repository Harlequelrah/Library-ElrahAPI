from typing import Optional

from elrahapi.database.database_manager import DatabaseManager
from elrahapi.database.session_manager import SessionManager
from .secret import (
    DATABASE,
    DATABASE_ASYNC_CONNECTOR,
    DATABASE_CONNECTOR,
    DATABASE_NAME,
    DATABASE_PASSWORD,
    DATABASE_SERVER,
    DATABASE_USERNAME,
)
from sqlalchemy.ext.declarative import declarative_base
database = DatabaseManager(
    database=DATABASE,
    database_username=DATABASE_USERNAME,
    database_password=DATABASE_PASSWORD,
    database_connector=DATABASE_CONNECTOR,
    database_async_connector=DATABASE_ASYNC_CONNECTOR,
    database_name=DATABASE_NAME,
    database_server=DATABASE_SERVER,
)

session_manager: Optional[SessionManager] = None
try:
    database.create_database_if_not_exists()
finally:
    Base = declarative_base()
    session_manager = database.create_session_maker()
    database.session_manager = session_manager
    database.base=Base

print(f"{session_manager.is_async_env}")
