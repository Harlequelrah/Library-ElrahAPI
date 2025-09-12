from pydantic import BaseModel
from elrahapi.authorization.base_meta_model import MetaAuthorizationBaseModel


class UserPrivilegeInUser(BaseModel):
    privilege: MetaAuthorizationBaseModel
    is_active: bool
