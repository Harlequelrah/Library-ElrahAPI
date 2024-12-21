from harlequelrah_fastapi.exception.custom_http_exception import CustomHttpException
from fastapi import HTTPException, status

HTTP_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
AUTHENTICATION_EXCEPTION = CustomHttpException(HTTP_EXCEPTION)
