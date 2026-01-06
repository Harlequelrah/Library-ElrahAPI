import sys

from app.settings.auth.cruds import privilege_crud
from app.settings.config.database_config import session_manager
from app.settings.config.seeders_logger_config import SEEDERS_LOGS, seeders_logger
from elrahapi.authorization.privilege.schemas import PrivilegeCreateModel
from elrahapi.database.seed_manager import Seed

data: list[PrivilegeCreateModel] = [
    PrivilegeCreateModel(
        name="CAN_DO_SPECIAL_1", description="Special privilege 1", is_active=True
    ),
    PrivilegeCreateModel(
        name="CAN_DO_SPECIAL_2", description="Special privilege 2", is_active=True
    ),
    PrivilegeCreateModel(
        name="CAN_DO_SPECIAL_3", description="Special privilege 3", is_active=True
    ),
    PrivilegeCreateModel(
        name="CAN DO ACTION 1", description="Can do action 1", is_active=True
    ),
    PrivilegeCreateModel(
        name="CAN DO ACTION 2", description="Can do action 2", is_active=True
    ),
    PrivilegeCreateModel(
        name="CAN DO ACTION 3", description="Can do action 3", is_active=True
    ),
    PrivilegeCreateModel(
        name="CAN DO ACTION 4", description="Can do action 4", is_active=True
    ),
]


privilege_seed = Seed(
    crud_forgery=privilege_crud,
    data=data,
    logger=seeders_logger,
    seeders_logs=SEEDERS_LOGS,
)
if __name__ == "__main__":
    session = session_manager.get_session_for_script()
    privilege_seed.run_seed(sys.argv, session)
    privilege_seed.run_seed(sys.argv, session)
