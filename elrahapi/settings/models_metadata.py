from myproject.settings.logger.model import LogModel
from myproject.settings.auth.models import (
    Role,
    RolePrivilege,
    User,
    UserPrivilege,
    UserRole,
)
from myproject.settings.database import Base, database_manager  # à importer en dernier


database_manager.create_tables(target_metadata=Base.metadata)
