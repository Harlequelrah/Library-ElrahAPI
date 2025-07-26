import sys
from elrahapi.database.seed_manager import Seed
from settings.auth.cruds import role_crud
from elrahapi.authorization.role.schemas import RoleCreateModel
from settings.database import database
from log.seeders_logger import seeders_logger, SEEDERS_LOGS

data: list[RoleCreateModel] = [
    RoleCreateModel(name="ADMIN", description="Administre le système", is_active=True),
    RoleCreateModel(name="MANAGER", description="Gère le système", is_active=True),
    RoleCreateModel(name="SECRETARY", description="Aide le système", is_active=False),
]

role_seed = Seed(
    crud_forgery=role_crud, data=data, logger=seeders_logger, seeders_logs=SEEDERS_LOGS
)
session = database.session_manager.get_session_for_script()
role_seed.run_seed(sys.argv, session)
