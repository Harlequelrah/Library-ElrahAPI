from pydantic import BaseSettings, ConfigDict


class ElrahSettings(BaseSettings):
    project_name: str
    database: str
    env: str = "development"
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

    @property
    def debug(self) -> bool:
        return self.environment == "development"
