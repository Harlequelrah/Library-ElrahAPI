from pydantic import BaseModel
from typing import List,Any
class BulkDeleteModel(BaseModel):
    delete_liste:List[Any]=[]
