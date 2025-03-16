from elrahapi.authentication.authentication_router_provider import AuthenticationRouterProvider
from .database import authentication
from myproject.userapp.cruds import user_crud_models

authentication.authentication_models=user_crud_models

authentication_router_provider = AuthenticationRouterProvider(authentication=authentication)
authentication_router = authentication_router_provider.get_auth_router()







