import sys
from elrahapi.database.seed_manager import Seed
from settings.auth.cruds import user_role_crud
from elrahapi.authorization.user_role.schemas import UserRoleCreateModel
from settings.database import database
from log.seeders_logger import seeders_logger, SEEDERS_LOGS

data: list[UserRoleCreateModel] = [
    UserRoleCreateModel(
        user_id=1,
        role_id=1,
        is_active=True,
    ),
    UserRoleCreateModel(
        user_id=2,
        role_id=2,
        is_active=True,
    ),
    UserRoleCreateModel(
        user_id=3,
        role_id=3,
        is_active=True,
    )
]

user_role_seed = Seed(
    crud_forgery=user_role_crud,
    data=data,
    logger=seeders_logger,
    seeders_logs=SEEDERS_LOGS,
)

if __name__ == "__main__":
    session = database.session_manager.get_session_for_script()
    user_role_seed.run_seed(sys.argv, session)
