from typing import Optional
from fastapi.responses import JSONResponse
from harlequelrah_fastapi.exception.custom_http_exception import CustomHttpException as CHE
from fastapi import HTTPException as HE,status
from harlequelrah_fastapi.utility.utils import update_entity
from sqlalchemy import func
from sqlalchemy.orm import Session
class CrudForgery :
    def __init__(self,entity_name:str,session_factory,SQLAlchemyModel,CreatePydanticModel=None,UpdatePydanticModel=None):
        self.SQLAlchemyModel = SQLAlchemyModel
        self.CreatePydanticModel=CreatePydanticModel
        self.UpdatePydanticModel=UpdatePydanticModel
        self.session_factory = session_factory
        self.entity_name=entity_name
    async def create(self,create_obj):
        if isinstance(create_obj,self.CreatePydanticModel):
            session= self.session_factory()
            new_obj=self.SQLAlchemyModel(**create_obj.dict())
            try :
                session.add(new_obj)
                session.commit()
                session.refresh(new_obj)
                return new_obj
            except Exception as e:
                session.rollback()
                detail=f"Error occurred while creating {self.entity_name} , details : {str(e)}"
                http_exception=HE(status_code=status.HTTP_400_BAD_REQUEST,detail=detail)
                custom_http_exception=CHE(http_exception=http_exception)
                raise custom_http_exception
        else :
            detail=f"Invalid {self.entity_name} object for creation"
            http_exception=HE(status_code=status.HTTP_400_BAD_REQUEST,detail=detail)
            custom_http_exception=CHE(http_exception=http_exception)
            raise custom_http_exception

    async def count(self)->int:
        session=self.session_factory()
        try :
            count=session.query(func.count(self.SQLAlchemyModel.id)).scalar()
            return count
        except Exception as e:
            detail=f"Error occurred while counting {self.entity_name}s , details : {str(e)}"
            http_exception=HE(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=detail)
            custom_http_exception=CHE(http_exception=http_exception)
            raise custom_http_exception

    async def read_all(self,skip:int=0,limit:int=None):
        session=self.session_factory()
        if limit is None : limit = await self.count()
        return session.query(self.SQLAlchemyModel).offset(skip).limit(limit).all()

    async def validate_filter_value(self,value):
        if value in ["true","True"]: value = True
        elif value in ["false","False"]: value = False
        elif value.isdigit():
            value = int(value)
        return value


    async def read_all_by_filter(self,filter,value,skip:int=0,limit:int=None):
        session=self.session_factory()
        if limit is None : limit = await self.count()
        exist_filter = getattr(self.SQLAlchemyModel,filter,None)
        if exist_filter:
            value = await self.validate_filter_value(value)
            return session.query(self.SQLAlchemyModel).filter(exist_filter==value).offset(skip).limit(limit).all()
        else :
            detail = f"Invalid filter {filter} for entity {self.entity_name}"
            http_exception=HE(status_code=status.HTTP_400_BAD_REQUEST,detail=detail)
            custom_http_exception=CHE(http_exception=http_exception)
            raise custom_http_exception

    async def read_one(self,id:int,db:Optional[Session]=None):
        if db : session=db
        else: session=self.session_factory()
        read_obj=session.query(self.SQLAlchemyModel).filter(self.SQLAlchemyModel.id==id).first()
        if read_obj is None:
            detail=f"{self.entity_name} with id {id} not found"
            http_exc = HE(status_code=status.HTTP_404_NOT_FOUND,detail=detail)
            custom_http_exception = CHE(http_exc)
            raise custom_http_exception
        return read_obj

    async def update(self,id:int,update_obj):
        if isinstance(update_obj,self.UpdatePydanticModel):
            session=self.session_factory()
            try :
                existing_obj=await self.read_one(id,session)
                existing_obj=update_entity(existing_entity=existing_obj,update_entity=update_obj)
                session.commit()
                session.refresh(existing_obj)
                return existing_obj
            except Exception as e:
                session.rollback()
                detail=f"Error occurred while updating {self.entity_name} with id {id} , details : {str(e)}"
                http_exception=HE(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=detail)
                custom_http_exception=CHE(http_exception=http_exception)
                raise custom_http_exception
        else:
            detail=f"Invalid {self.entity_name}  object for update"
            http_exception=HE(status_code=status.HTTP_400_BAD_REQUEST,detail=detail)
            custom_http_exception=CHE(http_exception=http_exception)
            raise custom_http_exception

    async def delete(self,id):
        session=self.session_factory()
        try :
            existing_obj=await self.read_one(id,session)
            session.delete(existing_obj)
            session.commit()
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            session.rollback()
            detail=f"Error occurred while deleting {self.entity_name} with id {id} , details : {str(e)}"
            http_exception=HE(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=detail)
            custom_http_exception=CHE(http_exception=http_exception)
            raise custom_http_exception
