from pydantic import BaseModel
from elrahapi.authorization.base_meta_model import MetaAuthorizationBaseModel


class UserRoleInUser(BaseModel):
    role: MetaAuthorizationBaseModel
    is_active: bool
