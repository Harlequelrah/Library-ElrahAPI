from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from elrahapi.session.session_manager import SessionManager
from .secret import authentication,database
from elrahapi.utility.utils import create_database_if_not_exists

session_manager:Optional[SessionManager]=None
try:
    if database != 'sqlite':
        DATABASE_URL = f"{authentication.connector}://{authentication.database_username}:{authentication.database_password}@{authentication.server}"
        create_database_if_not_exists(DATABASE_URL, authentication.database_name)

finally:
    if  database == 'sqlite':
        DATABASE_URL = f"sqlite://"
        db_name = authentication.database_name if authentication.database_name else "database"
        SQLALCHEMY_DATABASE_URL = f"{DATABASE_URL}/{db_name}.db"
    else :
        SQLALCHEMY_DATABASE_URL = f"{DATABASE_URL}/{authentication.database_name}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
    sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    session_manager = SessionManager(session_factory=sessionLocal)
    authentication.session_manager=session_manager
