from settings.auth.models import (
    LogModel,
    Role,
    RolePrivilege,
    User,
    UserPrivilege,
    UserRole,
)
from settings.database import Base, database  # à importer en dernier

# from settings.logger.model import LogModel


database.create_tables(target_metadata=Base.metadata)
