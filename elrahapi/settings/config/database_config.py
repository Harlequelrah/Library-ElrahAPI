from elrahapi.database.database_manager import DatabaseManager
from myproject.settings.config.env_config import settings


database_manager = DatabaseManager(settings=settings)

try:
    database_manager.create_database_if_not_exists()
finally:
    session_manager = database_manager.create_session_manager()



