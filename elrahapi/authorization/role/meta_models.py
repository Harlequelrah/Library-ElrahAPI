from pydantic import BaseModel

from elrahapi.user.schemas import UserInRoleUser


class RoleUserInRole(BaseModel):
    user:UserInRoleUser
    is_active: bool
