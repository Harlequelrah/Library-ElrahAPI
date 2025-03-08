from pydantic import BaseModel

class BulkDeleteModel(BaseModel):
    delete_liste:list=[]
