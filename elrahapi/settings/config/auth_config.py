from app.settings.auth.cruds import user_crud_models
from app.settings.config.database_config import session_manager
from app.settings.config.env_config import settings
from elrahapi.authentication.authentication_manager import AuthenticationManager

user_crud_models.sqlalchemy_model.MAX_ATTEMPT_LOGIN = settings.user_max_attempt_login
authentication = AuthenticationManager(
    settings=settings,
    session_manager=session_manager,
    authentication_models=user_crud_models,
)
