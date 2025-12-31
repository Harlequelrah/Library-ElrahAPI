from elrahapi.database.database_manager import DatabaseManager
from sqlalchemy.orm import declarative_base

from .secret import settings

database = DatabaseManager(settings=settings)

try:
    database.create_database_if_not_exists()
finally:
    database.create_session_manager()
    Base = declarative_base()
