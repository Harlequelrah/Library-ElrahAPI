from typing import Optional

from elrahapi.database.database_manager import DatabaseManager
from elrahapi.database.session_manager import SessionManager
from elrahapi.utility.utils import create_database_if_not_exists
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .
from .secret import (
    DATABASE,
    DATABASE_ASYNC_CONNECTOR,
    DATABASE_CONNECTOR,
    DATABASE_NAME,
    DATABASE_PASSWORD,
    DATABASE_SERVER,
    DATABASE_USERNAME,
)

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
    if database != "sqlite":
        database.create_database_if_not_exists()
finally:
    if database == "sqlite":
        DATABASE_URL = f"sqlite://"
        db_name = database.database_name if database.database_name else "database"
        SQLALCHEMY_DATABASE_URL = f"{DATABASE_URL}/{db_name}.db"
    else:
        SQLALCHEMY_DATABASE_URL = f"{DATABASE_URL}/{database.database_name}"
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
    sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    session_manager = SessionManager(session_maker=sessionLocal)
    database.session_manager = session_manager

    authentication.session_manager=session_manger
    Base = declarative_base()
