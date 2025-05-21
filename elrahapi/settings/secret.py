import os
from typing import Optional

from dotenv import load_dotenv
from elrahapi.utility.utils import get_env_int

load_dotenv(".env")


DATABASE = os.getenv("DATABASE")
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_CONNECTOR = os.getenv("DATABASE_CONNECTOR")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_ASYNC_CONNECTOR = os.getenv("DATABASE_ASYNC_CONNECTOR")
DATABASE_SERVER = os.getenv("DATABASE_SERVER")

USER_MAX_ATTEMPT_LOGIN: Optional[int] = get_env_int("USER_MAX_ATTEMPT_LOGIN")
ACCESS_TOKEN_EXPIRATION: Optional[int] = get_env_int("ACCESS_TOKEN_EXPIRATION")
REFRESH_TOKEN_EXPIRATION: Optional[int] = get_env_int("REFRESH_TOKEN_EXPIRATION")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
