from pydantic import BaseModel
from elrahapi.authorization.base_meta_model import MetaAuthorizationBaseModel
class MetaUserPrivilegeModel(BaseModel):
    privilege:MetaAuthorizationBaseModel
    is_active:bool
