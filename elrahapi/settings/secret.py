from pydantic import ConfigDict

from elrahapi.elrahsettings.models import ElrahSettings


class Settings(ElrahSettings):
    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
