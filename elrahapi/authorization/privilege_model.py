from typing import List, Optional
from pydantic import BaseModel, Field


from elrahapi.authorization.meta_model import MetaAuthorization, MetaAuthorizationReadModel,MetaAuthorizationBaseModel


class PrivilegeModel(MetaAuthorization):
    pass


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

class PrivilegeFullReadModel(PrivilegeReadModel):
    privilege_roles:Optional[List["MetaAuthorizationBaseModel"]] = []
    privilege_users : Optional[List["MetaPrivilegeUsers"]] = []
    class Config :
        from_attributes=True


class MetaPrivilegeUsers(BaseModel):
    user_id:int
    is_active:bool



