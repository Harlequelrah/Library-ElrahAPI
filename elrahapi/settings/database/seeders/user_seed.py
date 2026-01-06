import sys

from elrahapi.database.seed_manager import Seed
from myproject.settings.auth.cruds import user_crud
from myproject.settings.auth.schemas import UserCreateModel
from myproject.settings.config.database_config import session_manager
from myproject.settings.config.env_settings import settings
from myproject.settings.config.seeders_logger_config import SEEDERS_LOGS, seeders_logger

data: list[UserCreateModel] = [
    UserCreateModel(
        email="admin@test.com",
        username="admin",
        password="admin@test" + settings.secret_key[0:4],
        firstname="Admin",
        lastname="User",
    ),
    UserCreateModel(
        email="manager@test.com",
        username="manager",
        password="manager@test" + settings.secret_key[0:4],
        firstname="Manager",
        lastname="User",
    ),
    UserCreateModel(
        email="secretary@test.com",
        username="secretary",
        password="secretary@test" + settings.secret_key,
        firstname="Secretary",
        lastname="User",
    ),
]

user_seed = Seed(
    crud_forgery=user_crud, data=data, logger=seeders_logger, seeders_logs=SEEDERS_LOGS
)

if __name__ == "__main__":
    session = session_manager.get_session_for_script()
    user_seed.run_seed(sys.argv, session)
