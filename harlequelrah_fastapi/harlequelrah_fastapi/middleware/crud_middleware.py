import time
from fastapi import Request
from sqlalchemy.orm import Session


async def save_log(
    request: Request,call_next, LoggerMiddlewareModel, db: Session,error=None
):
    if request.url.path in ["/openapi.json", "/docs", "/redoc", "/favicon.ico","/"]:
        return await call_next(request)
    start_time= time.time()
    response = await call_next(request)
    process_time=time.time() - start_time
    logger = LoggerMiddlewareModel(
    process_time=process_time,
    status_code=response.status_code,
    url=str(request.url),
    method=request.method,
    error_message=error,
    remote_address=str(request.client.host))
    db.add(logger)
    db.commit()
    db.refresh(logger)
    return response
