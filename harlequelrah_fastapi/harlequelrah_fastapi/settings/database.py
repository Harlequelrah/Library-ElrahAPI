from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .secret import authentication
connector = "mysql+mysqlconnector"
database_name = "mydatabase"
server = "localhost:3306"
SQLALCHEMY_DATABASE_URL = (
    f"{connector}://{authentication.database_username}:{authentication.database_password}@{server}/{database_name}"
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
