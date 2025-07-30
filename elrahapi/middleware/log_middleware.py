from elrahapi.authentication.authentication_manager import AuthenticationManager
from elrahapi.database.session_manager import SessionManager
from elrahapi.middleware.crud_middleware import save_log
from elrahapi.middleware.middleware_helper import MiddlewareHelper
from elrahapi.websocket.connection_manager import ConnectionManager
from starlette.middleware.base import BaseHTTPMiddleware

from fastapi import Request


class LoggerMiddleware(BaseHTTPMiddleware):

    def __init__(self, app,middleware_helper:MiddlewareHelper ):
        super().__init__(app)
        if middleware_helper.session_manager is None:
            raise ValueError("Session Manager must be provided for LoggerMiddleware")
        self.middleware_helper = middleware_helper

    async def dispatch(self, request : Request, call_next):
        try:
            return await save_log(
                authentication=self.middleware_helper.authentication,
                request=request,
                call_next=call_next,
                LogModel=self.middleware_helper.LogModel,
                session_manager=self.middleware_helper.session_manager,
                websocket_manager=self.middleware_helper.websocket_manager
                )
        except Exception as e:
            return await save_log(
                request=request,
                call_next=call_next,
                LogModel= self.middleware_helper.LogModel,
                session_manager=self.middleware_helper.session_manager,
                error=f"error during saving log , detail :{str(e)}",
                websocket_manager=self.middleware_helper.websocket_manager
                )
