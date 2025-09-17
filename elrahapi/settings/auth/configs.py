from elrahapi.authentication.authentication_manager import AuthenticationManager
from elrahapi.authentication.authentication_router_provider import (
    AuthenticationRouterProvider,
)
from settings.database import database
from settings.secret import (
    ACCESS_TOKEN_EXPIRATION,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRATION,
    SECRET_KEY,
    TEMP_TOKEN_EXPIRATION,
    USER_MAX_ATTEMPT_LOGIN,
)

from .cruds import user_crud_models

user_crud_models.sqlalchemy_model.MAX_ATTEMPT_LOGIN = USER_MAX_ATTEMPT_LOGIN
authentication = AuthenticationManager(
    secret_key=SECRET_KEY,
    algorithm=ALGORITHM,
    access_token_expiration=ACCESS_TOKEN_EXPIRATION,
    refresh_token_expiration=REFRESH_TOKEN_EXPIRATION,
    temp_token_expiration=TEMP_TOKEN_EXPIRATION,
    session_manager=database.session_manager,
    authentication_models=user_crud_models,
)


authentication_router_provider = AuthenticationRouterProvider(
    authentication=authentication,
)
authentication_router = authentication_router_provider.get_auth_router()
