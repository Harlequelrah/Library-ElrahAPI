from settings.seeders.user_seed import user_seed
from settings.seeders.role_seed import role_seed
from settings.seeders.privilege_seed import privilege_seed
from settings.seeders.user_role_seed import user_role_seed
from settings.seeders.role_privilege_seed import role_privilege_seed
from settings.seeders.user_privilege_seed import user_privilege_seed
from settings.database import database
from elrahapi.database.seed_manager import SeedManager
import sys

seeds_dict = {
    "user_seed":user_seed,
    "role_seed": role_seed,
    "privilege_seed": privilege_seed,
    "role_privilege_seed": role_privilege_seed,
    "user_role_seed": user_role_seed,
    "user_privilege_seed": user_privilege_seed,
}

seed_manager = SeedManager(
    seeds_dict=seeds_dict,
    session_manager=database.session_manager,
)

seeds_name = [] # Remplir pour exécuter des seeds spécifiques
seed_manager.run_seed_manager(argv=sys.argv, seeds_name=seeds_name)
