from typing import List, Optional
from pydantic import BaseModel, Field


from elrahapi.authorization.meta_model import MetaAuthorization, MetaAuthorizationPydanticModel,MetaAuthorizationBaseModel


class PrivilegeModel(MetaAuthorization):
    pass


class PrivilegeBaseModel(BaseModel):
    name : str=Field(example='can_add_privilege')

class PrivilegeCreateModel(PrivilegeBaseModel):
    description:str=Field(example='allow privilege creation for privilege')



class PrivilegeUpdateModel(BaseModel):
    name: Optional[str] = Field(example="can_add_privilege")
    is_active:Optional[bool]=Field(default=True,example=True)
    description:str=Field(example='allow privilege creation for privilege')





class PrivilegePydanticModel(MetaAuthorizationPydanticModel):
    roles:Optional[List["MetaAuthorizationBaseModel"]] = []
    privilege_users : Optional[List["MetaPrivilegeUsers"]] = []
    class Config :
        from_attributes=True
class MetaPrivilegeUsers(BaseModel):
    user_id:int
    is_active:bool



