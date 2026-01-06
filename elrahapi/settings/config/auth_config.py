from elrahapi.authentication.authentication_manager import AuthenticationManager
from elrahapi.authentication.authentication_router_provider import (
    AuthenticationRouterProvider,
)
from myproject.settings.auth.cruds import user_crud_models
from myproject.settings.config.database_config import session_manager
from myproject.settings.config.env_config import settings

user_crud_models.sqlalchemy_model.MAX_ATTEMPT_LOGIN = settings.user_max_attempt_login
authentication = AuthenticationManager(
    settings=settings,
    session_manager=session_manager,
    authentication_models=user_crud_models,
)


authentication_router_provider = AuthenticationRouterProvider(
    authentication=authentication,
)
authentication_router = authentication_router_provider.get_auth_router()
