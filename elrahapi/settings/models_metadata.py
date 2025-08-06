from settings.database import Base, database
from auth.models import User, Role, UserRole, UserPrivilege, RolePrivilege
from logger.model import LogModel


database.create_tables(target_metadata=Base.metadata)
