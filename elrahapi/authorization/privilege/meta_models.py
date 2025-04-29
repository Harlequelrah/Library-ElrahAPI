from pydantic import BaseModel


class MetaPrivilegeUsers(BaseModel):
    user_id:int
    is_active:bool
