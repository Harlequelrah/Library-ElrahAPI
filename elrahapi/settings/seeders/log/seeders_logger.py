import logging

from ...secret import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(settings.seeders_logs, mode="a", encoding="utf-8"),
    ],
)

seeders_logger = logging.getLogger("seeders")
