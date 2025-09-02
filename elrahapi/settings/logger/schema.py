from pydantic import ConfigDict
from elrahapi.middleware import models


class LogReadModel(models.MetaLogReadModel):
    # user_id: int | None = None
    model_config = ConfigDict(from_attributes=True)


# Vous pouvez adapter le type de subject à votre model pour qu'elle corresponde à votre modèle de validation
