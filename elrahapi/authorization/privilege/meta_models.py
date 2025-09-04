from pydantic import BaseModel

from elrahapi.user.schemas import UserInPrivilegeUser


class PrivilegeUserInPrivilege(BaseModel):
    user:UserInPrivilegeUser
    is_active:bool
