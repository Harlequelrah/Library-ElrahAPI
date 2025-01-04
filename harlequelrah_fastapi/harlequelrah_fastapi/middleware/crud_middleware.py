import json
import time
from fastapi import Request , status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from starlette.responses import Response
from harlequelrah_fastapi.websocket.connectionManager import ConnectionManager
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
    request: Request,LoggerMiddlewareModel, db: Session,call_next=None,error=None,response:Response=None,manager:ConnectionManager=None
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
        if error is not None and manager is not None:
            message=f"An error occurred during the request with the status code {response.status_code}, please check the log {logger.id} for more information"
            if manager is not None:
                await manager.send_message(message)
    except Exception as err:
        db.rollback()
        error_message= f"error : An unexpected error occurred during saving log , details : {str(err)}"
        print(error_message)
    return response


async def save_current_log(
    request: Request,LoggerMiddlewareModel, db: Session,call_next,error=None
):
    if request.url.path in ["/openapi.json", "/docs", "/redoc", "/favicon.ico","/"]:
        return await call_next(request)
    start_time=time.time()
    response = await call_next(request)
    process_time=time.time() - start_time
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
    except Exception as err:
        db.rollback()
        logger.error_message= f"error : An unexpected error occurred during saving log , details : {str(err)}"
        db.add(logger)
        db.commit()
        db.refresh(logger)
    return response
