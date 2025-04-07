from typing import List, Optional
from elrahapi.user import  schemas

class UserBaseModel(schemas.UserBaseModel):
    pass

class UserCreateModel(schemas.UserCreateModel):
    pass

class UserUpdateModel(schemas.UserUpdateModel):
    pass

class UserPatchModel(schemas.UserPatchModel):
    pass

class UserPydanticModel(schemas.UserPydanticModel):
    class Config :
        from_attributes=True



