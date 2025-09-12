import os

from dotenv import load_dotenv
from elrahapi.utility.utils import validate_value

load_dotenv(".env")


DATABASE = os.getenv("DATABASE")
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_CONNECTOR = os.getenv("DATABASE_CONNECTOR")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_ASYNC_CONNECTOR = os.getenv("DATABASE_ASYNC_CONNECTOR")
DATABASE_SERVER = os.getenv("DATABASE_SERVER")
IS_ASYNC_ENV = validate_value(os.getenv("IS_ASYNC_ENV"))
USER_MAX_ATTEMPT_LOGIN: int | None = validate_value(os.getenv("USER_MAX_ATTEMPT_LOGIN"))
ACCESS_TOKEN_EXPIRATION: int | None = validate_value(
    os.getenv("ACCESS_TOKEN_EXPIRATION")
)
REFRESH_TOKEN_EXPIRATION: int | None = validate_value(
    os.getenv("REFRESH_TOKEN_EXPIRATION")
)
TEMP_TOKEN_EXPIRATION: int | None = validate_value(os.getenv("TEMP_TOKEN_EXPIRATION"))
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
