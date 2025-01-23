from elrahapi.middleware.models import LoggerMiddlewarePydanticModel
class LogBaseModel(LoggerMiddlewarePydanticModel):
    class setting:
        from_orm=True



