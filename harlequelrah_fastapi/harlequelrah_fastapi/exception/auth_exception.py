from harlequelrah_fastapi.exception.custom_http_exception import CustomHttpException
from fastapi import HTTPException, status

INVALID_CREDENTIALS_HTTP_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
INACTIVE_USER_HTTP_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="The account you are trying to access is not active",
    headers={"WWW-Authenticate": "Bearer"},
)

INVALID_CREDENTIALS_CUSTOM_HTTP_EXCEPTION = CustomHttpException(INVALID_CREDENTIALS_HTTP_EXCEPTION)
INACTIVE_USER_CUSTOM_HTTP_EXCEPTION = CustomHttpException(INACTIVE_USER_HTTP_EXCEPTION)
