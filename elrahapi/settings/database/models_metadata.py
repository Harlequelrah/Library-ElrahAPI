from myproject.settings.auth.models import (
    Role,
    RolePrivilege,
    User,
    UserPrivilege,
    UserRole,
)
from myproject.settings.config.database_config import (  # à importer en dernier
    database_manager,
)
from myproject.settings.database.base import Base  # à importer en dernier


from myproject.settings.logger.model import LogModel

database_manager.create_tables(target_metadata=Base.metadata)
