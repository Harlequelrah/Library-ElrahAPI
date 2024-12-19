from sqlalchemy import func
from sqlalchemy.orm import Session
from harlequelrah_fastapi.exception.custom_http_exception import CustomHttpException as CHE

from fastapi import HTTPException as HE,status

class LoggerCrud:
    def __init__(self,session_factory,LoggerModel):
        self.session_local = session_factory
        self.LoggerModel = LoggerModel

    async def get_count_logs(self):
        db=self.session_local()
        return db.query(func.count(self.LoggerModel.id)).scalar()

    async def get_log(self,log_id):
        db = self.session_local()
        log=db.query(self.LoggerModel).filter(self.LoggerModel.id==log_id).first()
        if log is None :
            http_exc=HE(status_code=status.HTTP_404_NOT_FOUND,detail=f"Log {log_id} not found")
            raise CHE(http_exception= http_exc)
        return log

    async def get_logs(self,skip:int=None,limit:int=None):
        db = self.session_local()
        if limit is None:limit = await  self.get_count_logs()
        logs = db.query(self.LoggerModel).offset(skip).limit(limit).all()
        if not logs:
            raise HE(status_code=status.HTTP_404_NOT_FOUND, detail="No logs found")
        return logs
