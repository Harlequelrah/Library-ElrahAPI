import time
from fastapi import Request
from sqlalchemy.orm import  Session
from fastapi import HTTPException as HE, Response, status, Depends
from starlette.middleware.base import BaseHTTPMiddleware
from .model import Logger
class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request : Request, call_next,db:Session):
        start_time= time.time()
        response = await call_next(request)
        process_time=time.time() - start_time
        logger = Logger(
            process_time=process_time,
            status_code=response.status_code,
            url=str(request.url),
            method=request.method,
            user_agent=request.headers.get('User-Agent'),
            db_name=db.bind.url.database,
        )
        try :
            db.add(logger)
            db.commit()
            db.refresh(logger)
        except Exception as e:
            db.rollback()
            raise HE(
            status_code=500,
            detail=f"Erreur lors de la création du log : {str(e)}")
        return response


