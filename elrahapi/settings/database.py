from elrahapi.database.database_manager import DatabaseManager
from sqlalchemy.orm import declarative_base

from myproject.settings.secret import settings

database_manager = DatabaseManager(settings=settings)

try:
    database_manager.create_database_if_not_exists()
finally:
    database = database_manager.create_session_manager()
    Base = declarative_base()
