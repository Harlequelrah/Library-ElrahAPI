import sys
from elrahapi.database.seed_manager import Seed
from myproject.myapp.cruds import myapp_crud
from myproject.myapp.schemas import EntityCreateModel
from myproject.settings.database import database
from myproject.settings.log.seeders_logger import seeders_logger, SEEDERS_LOGS

data: list[EntityCreateModel] = []

myapp_seed = Seed(
    crud_forgery=myapp_crud, data=data, logger=seeders_logger, seeders_logs=SEEDERS_LOGS
)

if __name__ == "__main__":
    session = database.session_manager.get_session_for_script()
    myapp_seed.run_seed(sys.argv, session)
