from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from elrahapi.middleware.crud_middleware import save_log
from elrahapi.session.session_manager import SessionManager
from elrahapi.websocket.connection_manager import ConnectionManager
class LoggerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app,LogModel, session_manager:SessionManager,manager:ConnectionManager=None ):
        super().__init__(app)
        self.session_manager=session_manager
        self.LogModel = LogModel
        self.manager = manager
    async def dispatch(self, request : Request, call_next):
        db=self.session_manager.yield_session()
        try:
            return await save_log(request=request,call_next=call_next,LogModel=self.LogModel,db=db,manager=self.manager)
        except Exception as e:
            db.rollback()
            return await save_log(request, call_next=call_next,LogModel= self.LogModel, db=db,error=f"error during saving log , detail :{str(e)}",manager=self.manager)
        finally:
            db.close()
