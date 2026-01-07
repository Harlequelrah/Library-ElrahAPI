from app.settings.auth.models import Role, RolePrivilege, User, UserPrivilege, UserRole
from app.settings.config.database_config import (  # à importer en dernier
    database_manager,
)
from app.settings.database.base import Base  # à importer en dernier
from app.settings.logger.model import LogModel

database_manager.create_tables(target_metadata=Base.metadata)
