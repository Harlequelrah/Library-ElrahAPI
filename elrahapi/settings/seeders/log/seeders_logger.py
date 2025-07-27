import logging
import os
from dotenv import load_dotenv
load_dotenv(".env")
# from  .secret  import SEEDERS_LOGS
SEEDERS_LOGS = os.getenv("SEEDERS_LOGS", "seeders.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(SEEDERS_LOGS, mode="a", encoding="utf-8"),
    ],
)

seeders_logger = logging.getLogger("seeders")
