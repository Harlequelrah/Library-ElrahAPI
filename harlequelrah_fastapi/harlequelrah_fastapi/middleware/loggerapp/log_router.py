
from fastapi import APIRouter
from log_crud import logCrud
app_logger=APIRouter(
    tags=['logs'],prefix='/logs'
)

@app_logger.get('/get-count-logs')
async def get_count_logs():
    return await logCrud.get_count_logs()

@app_logger.get('/get-log/{log_id}')
async def get_log(log_id:int):
    return await logCrud.get_log(log_id)

@app_logger.get('/get-logs')
async def get_logs(skip:int=None,limit:int=None):
    return await logCrud.get_logs()



