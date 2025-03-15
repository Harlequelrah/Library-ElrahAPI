from elrahapi.middleware.models import LoggerMiddlewarePydanticModel
class LogPydanticModel(LoggerMiddlewarePydanticModel):
    class setting:
        from_attributes=True



