import sys

from app.settings.auth.cruds import user_privilege_crud
from app.settings.config.database_config import session_manager
from app.settings.config.seeders_logger_config import SEEDERS_LOGS, seeders_logger
from elrahapi.authorization.user_privilege.schemas import UserPrivilegeCreateModel
from elrahapi.database.seed_manager import Seed

data: list[UserPrivilegeCreateModel] = [
    UserPrivilegeCreateModel(
        user_id=1,
        privilege_id=1,
        is_active=True,
    ),
    UserPrivilegeCreateModel(
        user_id=2,
        privilege_id=2,
        is_active=True,
    ),
    UserPrivilegeCreateModel(
        user_id=3,
        privilege_id=3,
        is_active=True,
    ),
]

user_privilege_seed = Seed(
    crud_forgery=user_privilege_crud,
    data=data,
    logger=seeders_logger,
    seeders_logs=SEEDERS_LOGS,
)

if __name__ == "__main__":
    session = session_manager.get_session_for_script()
    user_privilege_seed.run_seed(sys.argv, session)
