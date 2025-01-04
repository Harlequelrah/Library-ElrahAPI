from fastapi import Request
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse, StreamingResponse
from starlette.types import Scope, Receive, Send
from fastapi import HTTPException as HE
from harlequelrah_fastapi.middleware.crud_middleware import save_log
from harlequelrah_fastapi.exception.custom_http_exception import (
    CustomHttpException as CHE,
)
import time
from harlequelrah_fastapi.websocket.connectionManager import ConnectionManager

class ErrorHandlingMiddleware:
    def __init__(self, app, LoggerMiddlewareModel=None, session_factory=None , manager:ConnectionManager=None):
        self.app = app
        self.LoggerMiddlewareModel = LoggerMiddlewareModel
        self.session_factory = session_factory
        self.manager=manager
        self.has_log = self.session_factory and self.LoggerMiddlewareModel

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)

        db = self.session_factory() if self.has_log else None

        try:
            # Démarre le chronométrage
            request.state.start_time = time.time()
            # Appelle l'application principale
            await self.app(scope, receive, send)

        # except HE as http_exc :
        #     print("http excp")
        #     responsse = JSONResponse(
        #         status_code=http_exc.status_code,
        #         content={"detail": http_exc.detail},
        #     )
        #     if self.has_log:
        #         await save_log(
        #             request,
        #             self.LoggerMiddlewareModel,
        #             db,
        #             response=response,
        #             manager=self.manager,
        #             error=f"HTTP error , details : {str(http_exc.detail)}",
        #         )
        #     await response(scope, receive, send)
        except CHE as custom_http_exc:
            http_exc=custom_http_exc.http_exception
            # Gère une exception personnalisée
            response = JSONResponse(
                status_code=custom_http_exc.http_exception.status_code,
                content={"detail":http_exc.detail},
            )
            if self.has_log:
                await save_log(
                    request,
                    self.LoggerMiddlewareModel,
                    db,
                    response=response,
                    manager=self.manager,
                    error=f"Custom HTTP error , details : {str(http_exc.detail)}",
                )
            await response(scope, receive, send)
        except SQLAlchemyError as db_error:
            # Gère une erreur SQLAlchemy
            response = JSONResponse(
                status_code=500,
                content={"error": "Database error", "details": str(db_error)},
            )
            if self.has_log:
                await save_log(
                    request,
                    self.LoggerMiddlewareModel,
                    db,
                    response=response,
                    manager=self.manager,
                    error=f"Database error : details , {str(db_error)}",
                )
            await response(scope, receive, send)
        except Exception as exc:
            # Gère les erreurs générales
            response = JSONResponse(
                status_code=500,
                content={"error": "An unexpected error occurred", "details": str(exc)},
            )
            if self.has_log:
                await save_log(
                    request,
                    self.LoggerMiddlewareModel,
                    db,
                    response=response,
                    manager=self.manager,
                    error=f"An unexpected error occurred , details : {str(exc)}",
                )
            await response(scope, receive, send)
