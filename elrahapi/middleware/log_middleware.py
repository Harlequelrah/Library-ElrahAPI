from elrahapi.database.session_manager import SessionManager
from elrahapi.middleware.crud_middleware import save_log
from elrahapi.websocket.connection_manager import ConnectionManager
from starlette.middleware.base import BaseHTTPMiddleware

from fastapi import Request


class LoggerMiddleware(BaseHTTPMiddleware):

    def __init__(self, app,LogModel, session_manager:SessionManager,websocket_manager:ConnectionManager=None ):
        super().__init__(app)
        self.session_manager=session_manager
        self.LogModel = LogModel
        self.websocket_manager = websocket_manager

    async def dispatch(self, request : Request, call_next):
        db= await self.session_manager.yield_session()
        try:
            return await save_log(request=request,call_next=call_next,LogModel=self.LogModel,db=db,websocket_manager=self.websocket_manager)
        except Exception as e:
            db.rollback()
            return await save_log(request, call_next=call_next,LogModel= self.LogModel, db=db,error=f"error during saving log , detail :{str(e)}",websocket_manager=self.websocket_manager)
        finally:
            db.close()
            return await save_log(request, call_next=call_next,LogModel= self.LogModel, db=db,error=f"error during saving log , detail :{str(e)}",websocket_manager=self.websocket_manager)
