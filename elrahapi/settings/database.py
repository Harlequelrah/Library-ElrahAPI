from elrahapi.database.database_manager import DatabaseManager
from myproject.settings.secret import settings
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase

database_manager = DatabaseManager(settings=settings)

try:
    database_manager.create_database_if_not_exists()
finally:
    database = database_manager.create_session_manager()


class Base(DeclarativeBase):
    type_annotation_map = {str: String(30)}
