from pydantic import BaseModel
from typing import Any


class BulkDeleteModel(BaseModel):
    delete_list: list[Any] = []
