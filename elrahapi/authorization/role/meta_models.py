from pydantic import BaseModel

class MetaRoleUsers(BaseModel):
    user_id:int
    is_active:bool
