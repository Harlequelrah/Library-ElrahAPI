from elrahapi.user import schemas
from pydantic import ConfigDict, Field, BaseModel


class UserBaseModel(schemas.UserBaseModel):
    pass


class UserCreateModel(UserBaseModel, schemas.UserCreateModel):
    pass


class UserUpdateModel(UserBaseModel, schemas.UserUpdateModel):
    pass


class UserPatchModel(BaseModel, schemas.UserPatchModel):
    pass


class UserReadModel(UserBaseModel, schemas.UserReadModel):
    model_config = ConfigDict(from_attributes=True)


class UserFullReadModel(UserBaseModel, schemas.UserFullReadModel):
    model_config = ConfigDict(from_attributes=True)
