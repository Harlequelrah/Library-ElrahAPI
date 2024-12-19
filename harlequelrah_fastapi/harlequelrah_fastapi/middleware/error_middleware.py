from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from harlequelrah_fastapi.middleware.crud_middleware import save_log
from harlequelrah_fastapi.exception.custom_http_exception import CustomHttpException as CHE

class ErrorHandlingMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, LoggerMiddlewareModel=None, session_factory=None):
        super().__init__(app)
        self.session_factory = session_factory
        self.LoggerMiddlewareModel = LoggerMiddlewareModel
        self.has_log = self.session_factory and self.LoggerMiddlewareModel

    async def dispatch(self, request: Request, call_next):

        try:
            print("error middleware dispatch")
            if self.has_log:
                print('session factory and logger are defined')
            else :
                print(" session factory and logger not defined")
            return await call_next(request)
        except CHE as custom_http_exc:
            http_exc = custom_http_exc.http_exception
            print("error middleware dispatch http error")
            if self.has_log:
                print("fire")
                db = self.session_factory()
                await save_log(
                    request,
                    call_next,
                    self.LoggerMiddlewareModel,
                    db,
                    error=f"HTTP error , details : {str(http_exc.detail)}",
                )
            else:
                print("http water")
            return JSONResponse(
                status_code=http_exc.status_code, content={"detail": http_exc.detail}
            )
        # except SQLAlchemyError as db_error:
        #     print("error middleware dispatch sqlalchemy error")
        #     db = self.session_factory()
        #     if self.has_log:
        #         await save_log(
        #             request,
        #             call_next,
        #             self.LoggerMiddlewareModel,
        #             db,
        #             error=f"Database error : details , {str(db_error)}",
        #         )
        #     else:
        #         print("sqlalchemy water")
        #     return JSONResponse(
        #         status_code=500,
        #         content={"error": "Database error", "details": str(db_error)},
        #     )
        # except Exception as exc:
        #     print("error middleware dispatch unexpected error")
        #     if self.has_log:
        #         db = self.session_factory()
        #         await save_log(
        #             request,
        #             call_next,
        #             self.LoggerMiddlewareModel,
        #             db,
        #             error=f"An unexpected error occurred , details : {str(exc)}",
        #         )
        #     else:
        #         print("water unocuured error")
        #     return JSONResponse(
        #         status_code=500,
        #         content={"error": "An unexpected error occurred", "details": str(exc)},
        #     )
