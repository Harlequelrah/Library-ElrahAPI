from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .secret import authentication_provider
from elrahapi.utility.utils import create_database_if_not_exists

DATABASE_URL = f"{authentication_provider.connector}://{authentication_provider.database_username}:{authentication_provider.database_password}@{authentication_provider.server}"


try:
    create_database_if_not_exists(DATABASE_URL, authentication_provider.database_name)
finally:
    SQLALCHEMY_DATABASE_URL = f"{DATABASE_URL}/{authentication_provider.database_name}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
    sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    authentication_provider.session_factory=sessionLocal
