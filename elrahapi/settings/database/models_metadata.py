from app.settings.config.database_config import (  # à importer en dernier
    database_manager,
)
from app.settings.database.base import Base  # à importer en dernier

database_manager.create_tables(target_metadata=Base.metadata)
