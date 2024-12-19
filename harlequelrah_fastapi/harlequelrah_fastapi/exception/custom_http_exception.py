from fastapi import HTTPException


class CustomHttpException(HTTPException):
    def __init__(self,http_exception:HTTPException):
        self.http_exception = http_exception
