from pydantic import BaseModel
from elrahapi.authorization.base_meta_model import MetaAuthorizationBaseModel



class MetaUserRoleModel(BaseModel):
    role:MetaAuthorizationBaseModel
    is_active:bool
