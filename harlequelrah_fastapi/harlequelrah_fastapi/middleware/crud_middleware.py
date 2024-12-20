import time
from fastapi import Request
from sqlalchemy.orm import Session
from starlette.responses import Response
async def get_process_time(request:Request,call_next=None,response:Response=None):
    if call_next is None:
        process_time = (
            time.time() - request.state.start_time
            if hasattr(request.state, "start_time")
            else None
        )
        return [response,process_time]
    else:
        start_time=time.time()
        current_response = await call_next(request)
        process_time=time.time() - start_time
    return [current_response,process_time]

async def save_log(
    request: Request,LoggerMiddlewareModel, db: Session,call_next=None,error=None,response:Response=None
):
    if request.url.path in ["/openapi.json", "/docs", "/redoc", "/favicon.ico","/"]:
        if call_next is None:
            return
        else : return await call_next(request)
    response,process_time= await get_process_time(request,call_next,response)
    logger = LoggerMiddlewareModel(
    process_time=process_time,
    status_code=response.status_code,
    url=str(request.url),
    method=request.method,
    error_message=error,
    remote_address=str(request.client.host))
    try :
        db.add(logger)
        db.commit()
        db.refresh(logger)
    except Exception as db_error:
        print(f"Erreur lors de la sauvegarde du log : {str(db_error)}")
        db.rollback()
    return response


