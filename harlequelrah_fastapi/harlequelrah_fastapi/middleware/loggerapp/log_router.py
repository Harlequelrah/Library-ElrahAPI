from typing import List
from fastapi import APIRouter
from .log_crud import logCrud
from .log_schema import LoggerMiddlewarePydanticModel as LMPD
app_logger=APIRouter(
    tags=['logs'],prefix='/logs'
)

@app_logger.get('/get-count-logs')
async def get_count_logs():
    return await logCrud.get_count_logs()

@app_logger.get('/get-log/{log_id}',response_model=LMPD)
async def get_log(log_id:int):
    return await logCrud.get_log(log_id)

@app_logger.get('/get-logs',response_model=List[LMPD])
async def get_logs(skip:int=None,limit:int=None):
    return await logCrud.get_logs(skip=skip,limit=limit)



