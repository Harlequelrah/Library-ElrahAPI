from app.settings.config.env_config import settings
from elrahapi.database.database_manager import DatabaseManager

database_manager = DatabaseManager(settings=settings)

try:
    database_manager.create_database_if_not_exists()
finally:
    session_manager = database_manager.create_session_manager()
