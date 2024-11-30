import time
from fastapi import Request
from sqlalchemy.orm import  Session
from starlette.middleware.base import BaseHTTPMiddleware
class LoggerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app,LoggerMiddlewareModel, db_session:Session ):
        super().__init__(app)
        self.db_session=db_session
        self.LoggerMiddlewareModel = LoggerMiddlewareModel
    async def dispatch(self, request : Request, call_next):
        if request.url.path in ["/openapi.json", "/docs", "/redoc"]:
            return await call_next(request)
        try:
            db=self.db_session()
            start_time= time.time()
            response = await call_next(request)
            process_time=time.time() - start_time
            logger = self.LoggerMiddlewareModel(
                process_time=process_time,
                status_code=response.status_code,
                url=str(request.url),
                method=request.method,
                user_agent=request.headers.get("User-Agent"),
                )
            db.add(logger)
            db.commit()
            db.refresh(logger)
            return response
        except Exception as e:
            db.rollback()  # Annuler les changements en cas d'erreur
            raise e
        finally:
            db.close()  #
