import time
from fastapi import Request
from sqlalchemy.orm import  Session
from starlette.middleware.base import BaseHTTPMiddleware
from harlequelrah_fastapi.middleware.crud_middleware import save_log
class LoggerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app,LoggerMiddlewareModel, db_session:Session ):
        super().__init__(app)
        self.db_session=db_session
        self.LoggerMiddlewareModel = LoggerMiddlewareModel
    async def dispatch(self, request : Request, call_next):
        try:
            db=self.db_session()
            return await save_log(request,call_next,self.LoggerMiddlewareModel,db)
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()
