from fastapi import HTTPException as HE
from elrahapi.exception.custom_http_exception import CustomHttpException as CHE
def raise_custom_http_exception(status_code:int,detail:str):
    http_exception=HE(status_code=status_code,detail=detail)
    custom_http_exception=CHE(http_exception=http_exception)
    raise custom_http_exception
