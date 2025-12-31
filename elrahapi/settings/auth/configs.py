from elrahapi.authentication.authentication_manager import AuthenticationManager
from elrahapi.authentication.authentication_router_provider import (
    AuthenticationRouterProvider,
)
from settings.database import database
from settings.secret import settings

from .cruds import user_crud_models

user_crud_models.sqlalchemy_model.MAX_ATTEMPT_LOGIN = settings.user_max_attempt_login
authentication = AuthenticationManager(
    secret_key=settings.secret_key,
    algorithm=settings.algorithm,
    access_token_expiration=settings.access_token_expiration,
    refresh_token_expiration=settings.refresh_token_expiration,
    temp_token_expiration=settings.temp_token_expiration,
    session_manager=database.session_manager,
    authentication_models=user_crud_models,
)


authentication_router_provider = AuthenticationRouterProvider(
    authentication=authentication,
)
authentication_router = authentication_router_provider.get_auth_router()
