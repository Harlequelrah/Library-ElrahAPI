from elrahapi.user import  schemas
from pydantic import Field,BaseModel

class UserBaseModel(schemas.UserBaseModel):
    pass

class UserCreateModel(UserBaseModel, schemas.UserCreateModel):
    pass

class UserUpdateModel(UserBaseModel,schemas.UserUpdateModel):
    pass



class UserPatchModel(BaseModel,schemas.UserPatchModel):
    pass

class UserReadModel(UserBaseModel,schemas.UserReadModel):
    class Config :
        from_attributes=True


class UserFullReadModel(UserBaseModel,schemas.UserFullReadModel):
    class Config :
        from_attributes=True


