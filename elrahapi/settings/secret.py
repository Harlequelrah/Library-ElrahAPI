from dotenv import load_dotenv
import os

from elrahapi.authentication.authentication_manager import AuthenticationManager

load_dotenv(".env")


database= os.getenv("DATABASE")
database_username=os.getenv("DATABASE_USERNAME")
database_password = os.getenv("DATABASE_PASSWORD")
connector = os.getenv("DATABASE_CONNECTOR")
database_name = os.getenv("DATABASE_NAME")
server = os.getenv("DATABASE_SERVER")
user_max_attempt_login=os.getenv("USER_MAX_ATTEMPT_LOGIN")
MAX_ATTEMPT_LOGIN :int|None= int(user_max_attempt_login) if user_max_attempt_login else None
authentication = AuthenticationManager(
    database_username=database_username,
    database_password=database_password,
    connector=connector,
    database_name=database_name,
    server=server,
)
