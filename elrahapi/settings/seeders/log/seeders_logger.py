import logging

from myproject.settings.secret import settings

SEEDERS_LOGS = settings.seeders_logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(SEEDERS_LOGS, mode="a", encoding="utf-8"),
    ],
)

seeders_logger = logging.getLogger("seeders")
