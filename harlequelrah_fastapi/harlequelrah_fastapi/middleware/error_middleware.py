from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from harlequelrah_fastapi.middleware.crud_middleware import save_log
class ErrorHandlingMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, LoggerMiddlewareModel=None, db_session: Session=None):
        super().__init__(app)
        self.db_session = db_session
        self.LoggerMiddlewareModel = LoggerMiddlewareModel
        self.has_log= self.db_session and self.LoggerMiddlewareModel

    async def dispatch(self, request: Request, call_next):

        try:
            return await call_next(request)
        except SQLAlchemyError as db_error:
            if self.has_log:
                await save_log(
                request,call_next,self.LoggerMiddlewareModel,self.db_session(),error=f"Database error : details , {str(db_error)}"
                )
            return JSONResponse(
                status_code=500,
                content={"error": "Database error", "details": str(db_error)},
            )
        except HTTPException as http_exc:
            if self.has_log:
                await save_log(
                    request,
                    call_next,
                    self.LoggerMiddlewareModel,
                    self.db_session(),
                    error=f"HTTP error , details : {str(http_exc.detail)}",
                )
            return JSONResponse(
                status_code=http_exc.status_code, content={"detail": http_exc.detail}
            )
        except Exception as exc:
            if self.has_log:
                await save_log(
                    request,
                    call_next,
                    self.LoggerMiddlewareModel,
                    self.db_session(),
                    error=f"An unexpected error occurred , details : {str(exc)}",
                )
            return  JSONResponse(
                status_code=500,
                content={"error": "An unexpected error occurred", "details": str(exc)},
            )
