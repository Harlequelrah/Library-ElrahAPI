import time

from elrahapi.exception.custom_http_exception import CustomHttpException as CHE
from elrahapi.middleware.crud_middleware import save_log
from elrahapi.middleware.middleware_helper import MiddlewareHelper
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.types import Receive, Scope, Send

from fastapi import Request


class ErrorHandlingMiddleware:
    def __init__(self, app, middleware_helper: MiddlewareHelper | None=None):
        self.app = app
        self.middleware_helper = middleware_helper
        self.has_log = (
            self.middleware_helper is not None
            and self.middleware_helper.session_manager
            and self.middleware_helper.LogModel
        )

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] not in ("http"):
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive=receive)
        try:
            request.state.start_time = time.time()
            await self.app(scope, receive, send)
        except CHE as custom_http_exc:
            http_exc = custom_http_exc.http_exception
            response = self._create_json_response(
                http_exc.status_code, {"detail": http_exc.detail}
            )
            await self._log_error(
                request, response, f"Custom HTTP error: {http_exc.detail}"
            )
            await response(scope, receive, send)
        except SQLAlchemyError as db_error:
            response = self._create_json_response(
                500, {"error": "Database error", "details": str(db_error)}
            )
            await self._log_error(request, response, f"Database error: {db_error}")
            await response(scope, receive, send)
        except Exception as exc:
            response = self._create_json_response(
                500, {"error": "Unexpected error", "details": str(exc)}
            )
            await self._log_error(request, response, f"Unexpected error: {exc}")
            await response(scope, receive, send)

    def _create_json_response(self, status_code, content):
        return JSONResponse(status_code=status_code, content=content)

    async def _log_error(self, request, response, error):
        if self.has_log:
            await save_log(
                authentication=self.middleware_helper.authentication,
                request=request,
                LogModel=self.middleware_helper.LogModel,
                session_manager=self.middleware_helper.session_manager,
                response=response,
                websocket_manager=self.middleware_helper.websocket_manager,
                error=error,
            )
