from typing import List, Optional
from elrahapi.user import  models

class UserBaseModel(models.UserBaseModel):
    pass

class UserCreateModel(models.UserCreateModel):
    pass

class UserUpdateModel(models.UserUpdateModel):
    pass

class UserPatchModel(models.UserPatchModel):
    pass

class UserPydanticModel(models.UserPydanticModel):
    class Config :
        from_attributes=True



