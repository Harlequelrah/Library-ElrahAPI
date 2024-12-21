from harlequelrah_fastapi.user import models
from settings import authentication
class UserBaseModel(models.UserBaseModel):
    pass

class UserCreateModel(models.UserCreateModel):
    pass

class UserUpdateModel(models.UserUpdateModel):
    pass

class AdditionalUserPydanticModelField(models.AdditionalUserPydanticModelField):
    pass

class UserPydanticModel(UserBaseModel,AdditionalUserPydanticModelField):
    pass

authentication.UserPydanticModel = UserPydanticModel
authentication.UserCreateModel = UserCreateModel
authentication.UserUpdateModel = UserUpdateModel


