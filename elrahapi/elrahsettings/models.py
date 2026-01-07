from pydantic import field_validator
from pydantic_settings import BaseSettings


class ElrahSettings(BaseSettings):
    project_name: str
    database: str
    environment: str = "development"
    database_username: str
    database_password: str
    database_connector: str
    database_name: str
    database_async_connector: str
    database_server: str
    is_async_env: bool | None
    user_max_attempt_login: int | None
    access_token_expiration: int | None
    refresh_token_expiration: int | None
    temp_token_expiration: int | None
    secret_key: str
    algorithm: str
    seeders_logs: str = "seeders.log"
    issuer: str
    audience: str
    redis_url:str|None

    @property
    def debug(self) -> bool:
        return self.environment == "development"

    @field_validator(
        "user_max_attempt_login",
        "access_token_expiration",
        "refresh_token_expiration",
        "temp_token_expiration",
        mode="before",
    )
    @classmethod
    def set_empty_string_to_none(cls, v):
        if v == "":
            return None
        return v
