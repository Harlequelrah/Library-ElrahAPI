from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .secret import authentication
from harlequelrah_fastapi.utility.database_utils import create_database_if_not_exists

DATABASE_URL = f"{authentication.connector}://{authentication.database_username}:{authentication.database_password}@{authentication.server}"


SQLALCHEMY_DATABASE_URL = create_database_if_not_exists(
    DATABASE_URL, authentication.database_name
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


authentication.set_db_session(session_factory=sessionLocal)
