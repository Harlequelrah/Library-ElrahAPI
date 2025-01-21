from harlequelrah_fastapi.authorization.meta_model import MetaAuthorization, MetaAuthorizationBaseModel,MetaAuthorizationPydanticModel
from pydantic import BaseModel, Field
from typing import List, Optional

from harlequelrah_fastapi.authorization.privilege_model import PrivilegeCreateModel




class RoleModel(MetaAuthorization):
    pass

class RoleBaseModel(BaseModel):
    name: str = Field(example="Admin")


class RoleCreateModel(RoleBaseModel):
    description:str=Field(example='allow to manage all the system')
    privileges:Optional[List[PrivilegeCreateModel]]


class RoleUpdateModel(BaseModel):
    name: Optional[str] = Field(example="Admin", default=None)
    is_active : Optional[bool] = Field(example=True, default=None)
    description:str=Field(example='allow to manage all the system')




class RolePydanticModel(MetaAuthorizationPydanticModel):
    privileges: List["MetaAuthorizationBaseModel"]=[]

    class Config:
        from_orm = True

