from pydantic import BaseModel
from harlequelrah_fastapi.middleware.model import LoggerPydanticModel
class LogBaseModel(LoggerPydanticModel):
    class setting:
        from_orm=True



