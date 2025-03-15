

from fastapi.security import OAuth2PasswordBearer
from elrahapi.crud.crud_models import CrudModels
from elrahapi.user.models import (
    UserPydanticModel,
    UserCreateModel,
    UserUpdateModel,
    UserPatchModel,
    UserModel as User,
)


TOKEN_URL = "users/tokenUrl"
OAUTH2_SCHEME = OAuth2PasswordBearer(TOKEN_URL)
REFRESH_TOKEN_EXPIRATION = 86400000
ACCESS_TOKEN_EXPIRATION = 3600000
USER_AUTH_MODELS = CrudModels(
        UserPydanticModel=UserPydanticModel,
        UserSQLAlchemyModel=User,
        UserCreateModel=UserCreateModel,
        UserUpdateModel=UserUpdateModel,
        UserPatchModel=UserPatchModel,
)
