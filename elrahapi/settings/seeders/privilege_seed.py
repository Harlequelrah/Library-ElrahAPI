import sys

from elrahapi.authorization.privilege.schemas import PrivilegeCreateModel
from elrahapi.database.seed_manager import Seed
from log.seeders_logger import SEEDERS_LOGS, seeders_logger
from settings.auth.cruds import privilege_crud
from settings.database import database

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
    session = database.session_manager.get_session_for_script()
    privilege_seed.run_seed(sys.argv, session)
