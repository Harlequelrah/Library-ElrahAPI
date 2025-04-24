from typing import List, Optional
from elrahapi.user import  schemas
from pydantic import Field,BaseModel

class UserBaseModel(BaseModel,schemas.UserBaseModel):
    pass

class UserCreateModel(UserBaseModel, schemas.UserCreateModel):
    pass

class UserUpdateModel(UserBaseModel,schemas.UserUpdateModel):
    pass



class UserPatchModel(BaseModel,schemas.UserPatchModel):
    pass

class UserPydanticModel(UserBaseModel,schemas.UserPydanticModel):
    class Config :
        from_attributes=True



