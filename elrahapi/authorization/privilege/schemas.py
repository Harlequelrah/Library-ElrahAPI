from typing import List, Optional
from pydantic import BaseModel, Field

from elrahapi.authorization.base_meta_model import  MetaAuthorizationReadModel,MetaAuthorizationBaseModel

from elrahapi.authorization.privilege.meta_models import MetaPrivilegeUsers


class PrivilegeBaseModel(BaseModel):
    name : str=Field(example='can_add_privilege')
    description:str=Field(example='allow privilege creation for privilege')

class PrivilegeCreateModel(PrivilegeBaseModel):
    is_active:Optional[bool]=Field(default=True,example=True)

class PrivilegeUpdateModel(PrivilegeBaseModel):
    is_active:bool=Field(example=True)

class PrivilegePatchModel(BaseModel):
    name: Optional[str] = Field(example="can_add_privilege",default=None)
    is_active:Optional[bool]=Field(default=None,example=True)
    description:Optional[str]=Field(example='allow privilege creation for privilege',default=None)


class PrivilegeReadModel(MetaAuthorizationReadModel):
    class Config :
        from_attributes=True


class PrivilegeFullReadModel(MetaAuthorizationReadModel):
    privilege_roles:Optional[List["MetaAuthorizationBaseModel"]] = []
    privilege_users: Optional[List["MetaPrivilegeUsers"]] = []
    class Config :
        from_attributes=True
