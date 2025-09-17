from settings.logger.model import LogModel
from settings.auth.models import (
    Role,
    RolePrivilege,
    User,
    UserPrivilege,
    UserRole,
)
from settings.database import Base, database  # à importer en dernier


database.create_tables(target_metadata=Base.metadata)
