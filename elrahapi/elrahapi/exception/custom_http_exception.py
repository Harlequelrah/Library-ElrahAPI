from fastapi import HTTPException


class CustomHttpException(Exception):
    def __init__(self,http_exception:HTTPException):
        self.http_exception = http_exception
