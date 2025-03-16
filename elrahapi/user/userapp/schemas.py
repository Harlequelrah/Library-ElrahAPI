from typing import List, Optional
from elrahapi.authorization.meta_model import MetaUserPrivilegeModel
from elrahapi.user import  models

class UserBaseModel(models.UserBaseModel):
    pass

class UserCreateModel(models.UserCreateModel):
    pass

class UserUpdateModel(models.UserUpdateModel):
    pass

class UserPatchModel(models.UserPatchModel):
    pass

class UserPydanticModel(UserBaseModel):
    user_privileges: Optional[List["MetaUserPrivilegeModel"]]
    class Config :
        from_attributes=True



