from sqlalchemy import func
from sqlalchemy.orm import Session
from settings.logger_model import Logger
async def count_logs(db:Session):
    return db.query(func.count(Logger))
