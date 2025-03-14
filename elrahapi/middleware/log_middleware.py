from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from elrahapi.middleware.crud_middleware import save_log
from elrahapi.websocket.connection_manager import ConnectionManager
class LoggerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app,LoggerMiddlewareModel, session_factory,manager:ConnectionManager=None ):
        super().__init__(app)
        self.session_factory=session_factory
        self.LoggerMiddlewareModel = LoggerMiddlewareModel
        self.manager = manager
    async def dispatch(self, request : Request, call_next):
        try:
            db=self.session_factory()
            return await save_log(request=request,call_next=call_next,LoggerMiddlewareModel=self.LoggerMiddlewareModel,db=db,manager=self.manager)
        except Exception as e:
            db.rollback()
            return await save_log(request, call_next=call_next,LoggerMiddlewareModel= self.LoggerMiddlewareModel, db=db,error=f"error during saving log , detail :{str(e)}",manager=self.manager)
        finally:
            db.close()
