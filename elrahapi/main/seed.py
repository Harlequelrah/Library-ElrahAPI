import sys
from elrahapi.database.seed_manager import Seed
from myapp.cruds import myapp_crud
from myapp.schemas import EntityCreateModel
from settings.database import database
from log.seeders_logger import seeders_logger, SEEDERS_LOGS

data: list[EntityCreateModel] = []

myapp_seed = Seed(
    crud_forgery=myapp_crud, data=data, logger=seeders_logger, seeders_logs=SEEDERS_LOGS
)

session = database.session_manager.get_session_for_script()
myapp_seed.run_seed(sys.argv, session)
