from pydantic import BaseModel
from sqlalchemy import Boolean, Column,Integer,String,DateTime
from sqlalchemy.orm import validates
from sqlalchemy.sql import func
from datetime import datetime
class MetaAuthorization:
    id=Column(Integer,primary_key=True)
    name=Column(String(50),unique=True)
    description=Column(String(255),nullable=False)
    is_active=Column(Boolean,default=True)
    date_created = Column(DateTime, default=func.now())
    date_updated = Column(DateTime,default=func.now(), onupdate=func.now())

    @validates('name')
    def validate_name(self,key,value):
        return value.upper().strip() if value else None

class MetaAuthorizationBaseModel(BaseModel):
    is_active: bool

class MetaAuthorizationReadModel(MetaAuthorizationBaseModel):
    id:int
    name: str
    date_created: datetime
    date_updated:datetime
