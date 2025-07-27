from pydantic import BaseModel, Field

from elrahapi.authorization.base_meta_model import  MetaAuthorizationReadModel,MetaAuthorizationBaseModel

from elrahapi.authorization.privilege.meta_models import MetaPrivilegeUsers


class PrivilegeBaseModel(BaseModel):
    name : str=Field(example='can_add_privilege')
    description:str=Field(example='allow privilege creation for privilege')

class PrivilegeCreateModel(PrivilegeBaseModel):
    is_active:bool=Field(default=True,example=True)

class PrivilegeUpdateModel(PrivilegeBaseModel):
    is_active:bool=Field(example=True)

class PrivilegePatchModel(BaseModel):
    name: str | None = Field(example="can_add_privilege",default=None)
    is_active:bool|None=Field(default=None,example=True)
    description:str | None=Field(example='allow privilege creation for privilege',default=None)


class PrivilegeReadModel(MetaAuthorizationReadModel):
    class Config :
        from_attributes=True


class PrivilegeFullReadModel(MetaAuthorizationReadModel):
    privilege_roles:list["MetaAuthorizationBaseModel"]  | None = []
    privilege_users: list["MetaPrivilegeUsers"]  | None = []
    class Config :
        from_attributes=True
