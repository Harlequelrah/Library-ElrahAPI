import sys

from app.settings.config.database_config import session_manager
from app.settings.config.seeders_logger_config import SEEDERS_LOGS, seeders_logger
from elrahapi.authorization.role_privilege.schemas import RolePrivilegeCreateModel
from elrahapi.database.seed_manager import Seed
from settings.auth.cruds import role_privilege_crud

data: list[RolePrivilegeCreateModel] = [
    RolePrivilegeCreateModel(
        role_id=1,
        privilege_id=4,
        is_active=True,
    ),
    RolePrivilegeCreateModel(
        role_id=1,
        privilege_id=5,
        is_active=True,
    ),
    RolePrivilegeCreateModel(
        role_id=1,
        privilege_id=6,
        is_active=True,
    ),
    RolePrivilegeCreateModel(
        role_id=1,
        privilege_id=7,
        is_active=True,
    ),
    RolePrivilegeCreateModel(
        role_id=2,
        privilege_id=4,
        is_active=True,
    ),
    RolePrivilegeCreateModel(
        role_id=2,
        privilege_id=5,
        is_active=True,
    ),
    RolePrivilegeCreateModel(
        role_id=2,
        privilege_id=6,
        is_active=True,
    ),
    RolePrivilegeCreateModel(
        role_id=3,
        privilege_id=4,
        is_active=True,
    ),
]

role_privilege_seed = Seed(
    crud_forgery=role_privilege_crud,
    data=data,
    logger=seeders_logger,
    seeders_logs=SEEDERS_LOGS,
)

if __name__ == "__main__":
    session = session_manager.get_session_for_script()
    role_privilege_seed.run_seed(sys.argv, session)
    role_privilege_seed.run_seed(sys.argv, session)
