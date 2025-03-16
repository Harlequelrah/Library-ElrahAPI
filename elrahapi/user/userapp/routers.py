
from elrahapi.router.router_provider import CustomRouterProvider
from .cruds import user_crud,user_privilege_crud
from myproject.settings.auth_configs import authentication


user_router_provider = CustomRouterProvider(
    prefix="/users",
    tags=["users"],
    crud=user_crud,
    authentication=authentication,
)

user_privilege_router_provider=CustomRouterProvider(
    prefix='/users/privileges',
    tags=["users_privileges"],
    crud=user_privilege_crud,
    authentication=authentication,
)

user_router = user_router_provider.get_protected_router()

user_privilege_router=user_privilege_router_provider.get_protected_router()
