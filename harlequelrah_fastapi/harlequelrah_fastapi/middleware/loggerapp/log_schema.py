from pydantic import BaseModel
from harlequelrah_fastapi.middleware.model import LoggerMiddlewarePydanticModel
class LogBaseModel(LoggerMiddlewarePydanticModel):
    class setting:
        from_orm=True



