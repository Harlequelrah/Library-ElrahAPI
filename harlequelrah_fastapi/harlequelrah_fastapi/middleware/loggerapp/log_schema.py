from pydantic import BaseModel
from harlequelrah_fastapi.middleware.models import LoggerMiddlewarePydanticModel
class LogBaseModel(LoggerMiddlewarePydanticModel):
    class setting:
        from_orm=True



