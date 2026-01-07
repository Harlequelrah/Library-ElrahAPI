import sys

from app.myapp.cruds import myapp_crud
from app.myapp.schemas import EntityCreateModel
from app.settings.config.database_config import database_manager
from app.settings.config.seeders_logger_config import SEEDERS_LOGS, seeders_logger
from elrahapi.database.seed_manager import Seed

data: list[EntityCreateModel] = []

myapp_seed = Seed(
    crud_forgery=myapp_crud, data=data, logger=seeders_logger, seeders_logs=SEEDERS_LOGS
)

if __name__ == "__main__":
    session = database_manager.session_manager.get_session_for_script()
    myapp_seed.run_seed(sys.argv, session)
