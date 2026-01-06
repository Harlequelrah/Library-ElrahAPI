import sys

from app.settings.auth.cruds import role_crud
from app.settings.config.database_config import session_manager
from app.settings.config.seeders_logger_config import SEEDERS_LOGS, seeders_logger
from elrahapi.authorization.role.schemas import RoleCreateModel
from elrahapi.database.seed_manager import Seed

data: list[RoleCreateModel] = [
    RoleCreateModel(name="ADMIN", description="Administre le système", is_active=True),
    RoleCreateModel(name="MANAGER", description="Gère le système", is_active=True),
    RoleCreateModel(name="SECRETARY", description="Aide le système", is_active=False),
]

role_seed = Seed(
    crud_forgery=role_crud, data=data, logger=seeders_logger, seeders_logs=SEEDERS_LOGS
)

if __name__ == "__main__":
    session = session_manager.get_session_for_script()
    role_seed.run_seed(sys.argv, session)
