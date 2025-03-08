from elrahapi.router.router_crud import exclude_route
from elrahapi.router.router_namespace import (
    ROUTES_PROTECTED_CONFIG,
    DefaultRoutesName,
    USER_AUTH_CONFIG_ROUTES,
)
from .user_router_providers import user_router_provider,role_router_provider,privilege_router_provider,user_privilege_router_provider,role_privilege_router_provider





custom_init_data = USER_AUTH_CONFIG_ROUTES + exclude_route(ROUTES_PROTECTED_CONFIG,[DefaultRoutesName.CREATE])

app_user = user_router_provider.get_custom_public_router(
    init_data= custom_init_data ,
    public_routes_name=[DefaultRoutesName.CREATE],
)
# app_user=user_router_provider.get_public_router()
app_role = role_router_provider.get_protected_router()
app_privilege = privilege_router_provider.get_protected_router()
app_user_privilege=user_privilege_router_provider.get_protected_router()
app_role_privilege=role_privilege_router_provider.get_protected_router()
