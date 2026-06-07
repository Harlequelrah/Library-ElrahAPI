from pydantic_settings import SettingsConfigDict

from elrahapi.elrahsettings.models import ElrahSettings


class Settings(ElrahSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
