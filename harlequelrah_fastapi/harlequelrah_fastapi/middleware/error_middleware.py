import time
from fastapi import Request
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse
from fastapi import HTTPException as HE
from starlette.types import Scope, Receive, Send
from harlequelrah_fastapi.middleware.crud_middleware import get_process_time, save_log
from harlequelrah_fastapi.exception.custom_http_exception import (
    CustomHttpException as CHE,
)
from harlequelrah_fastapi.websocket.connectionManager import ConnectionManager


class ErrorHandlingMiddleware:
    def __init__(
        self,
        app,
        LoggerMiddlewareModel=None,
        session_factory=None,
        manager: ConnectionManager = None,
    ):
        self.app = app
        self.LoggerMiddlewareModel = LoggerMiddlewareModel
        self.session_factory = session_factory
        self.manager = manager
        self.has_log = self.session_factory and self.LoggerMiddlewareModel

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive=receive)
        db = self.session_factory() if self.has_log else None

        try:
            request.state.start_time = time.time()
            await self.app(scope, receive, send)
        except CHE as custom_http_exc:
            http_exc = custom_http_exc.http_exception
            response = self._create_json_response(
                http_exc.status_code, {"detail": http_exc.detail}
            )
            await self._log_error(
                request, db, response, f"Custom HTTP error: {http_exc.detail}"
            )
            await response(scope, receive, send)
        except SQLAlchemyError as db_error:
            response = self._create_json_response(
                500, {"error": "Database error", "details": str(db_error)}
            )
            await self._log_error(request, db, response, f"Database error: {db_error}")
            await response(scope, receive, send)
        except Exception as exc:
            response = self._create_json_response(
                500, {"error": "Unexpected error", "details": str(exc)}
            )
            await self._log_error(request, db, response, f"Unexpected error: {exc}")
            await response(scope,receive,send)
        finally:
            if db:
                db.close()

    def _create_json_response(self, status_code, content):
        return JSONResponse(status_code=status_code, content=content)

    async def _log_error(self, request, db, response, error):
        if self.has_log:
            await save_log(
                request=request,
                LoggerMiddlewareModel=self.LoggerMiddlewareModel,
                db=db,
                response=response,
                manager=self.manager,
                error=error,
            )
