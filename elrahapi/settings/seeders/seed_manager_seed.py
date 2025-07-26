from settings.seeders.role_seed import role_seed
from settings.database import database
from elrahapi.database.seed_manager import SeedManager
import sys

seeds_dict = {
    "role_seed": role_seed,
}
seed_manager = SeedManager(
    seeds_dict=seeds_dict,
    session_manager=database.session_manager,
)

seeds_name = ["role_seed"]
seed_manager.run_seed_manager(argv=sys.argv, seeds_name=seeds_name, full_seeds=False)
