import sys

from elrahapi.database.seed_manager import Seed
from myproject.settings.log.seeders_logger import SEEDERS_LOGS, seeders_logger
from myproject.settings.auth.cruds import user_crud
from myproject.settings.auth.schemas import UserCreateModel
from myproject.settings.database import database_manager
from myproject.settings.secret import SECRET_KEY  # .env

data: list[UserCreateModel] = [
    UserCreateModel(
        email="admin@test.com",
        username="admin",
        password="admin@test" + SECRET_KEY[0:4],
        firstname="Admin",
        lastname="User",
    ),
    UserCreateModel(
        email="manager@test.com",
        username="manager",
        password="manager@test" + SECRET_KEY[0:4],
        firstname="Manager",
        lastname="User",
    ),
    UserCreateModel(
        email="secretary@test.com",
        username="secretary",
        password="secretary@test" + SECRET_KEY[0:4],
        firstname="Secretary",
        lastname="User",
    ),
]

user_seed = Seed(
    crud_forgery=user_crud, data=data, logger=seeders_logger, seeders_logs=SEEDERS_LOGS
)

if __name__ == "__main__":
    session = database_manager.session_manager.get_session_for_script()
    user_seed.run_seed(sys.argv, session)
