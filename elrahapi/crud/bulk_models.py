from pydantic import BaseModel
from typing import Any
class BulkDeleteModel(BaseModel):
    delete_liste:list[Any]=[]
